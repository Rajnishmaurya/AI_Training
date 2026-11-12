"""
E-commerce Returns & Refund Processing
Microsoft Agent Framework + Azure OpenAI (SIMULATION - no payments/messages sent)

Graph:
  Return Request -> EligibilityExecutor -> RiskExecutor -> ApprovalGateway
                 -> CustomerResponseExecutor -> Final Output
  ApprovalGateway pauses (request_info) for human review and resumes
  via @response_handler with the manager's decision.
"""
import argparse
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from typing_extensions import Never

from agent_framework import (
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
    response_handler,
)

# ----------------------------------------------------------------------------
# Policy constants (deterministic business rules)
# ----------------------------------------------------------------------------
MAX_AUTO_AMOUNT = 25_000
MAX_DAYS = 30
MAX_PREV_RETURNS = 3  # must be fewer than this

POLICY_TEXT = f"""
Demonstration return policy - automatic approval only if ALL are true:
1. Product amount below Rs.{MAX_AUTO_AMOUNT:,}.
2. Request within {MAX_DAYS} days of delivery.
3. Customer invoice is available.
4. Item is unopened, or damaged with supporting photographs.
5. Fewer than {MAX_PREV_RETURNS} previous returns in the last 90 days.
6. Risk Agent has not identified a HIGH-risk concern.
Otherwise the request must be escalated for human review.
"""

REQUIRED_ENV = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_BASE_URL", "AZURE_OPENAI_MODEL"]


# ----------------------------------------------------------------------------
# Data models passed between executors
# ----------------------------------------------------------------------------
@dataclass
class CaseState:
    record: dict
    eligibility_issues: list[str] = field(default_factory=list)
    eligibility_findings: str = ""
    risk_level: str = "UNKNOWN"
    risk_assessment: str = ""
    route: str = ""
    decision: str = ""
    customer_message: str = ""


@dataclass
class ApprovalRequest:
    """Payload shown to the manager; carries the case so context is preserved."""
    request_id: str
    item: str
    amount: float
    eligibility_issues: list[str]
    risk_assessment: str
    case: CaseState


# ----------------------------------------------------------------------------
# Input loading / normalization (maps returns.json keys to workflow keys)
# ----------------------------------------------------------------------------
def normalize_record(raw: dict) -> dict:
    try:
        amount = float(raw["amount_inr"])
        if amount.is_integer():
            amount = int(amount)
        return {
            "request_id": str(raw["request_id"]),
            "order_id": str(raw["order_id"]),
            "product": raw["product"],
            "category": raw.get("product_category", ""),
            "request_type": str(raw["request_type"]).title(),  # REFUND -> Refund
            "amount": amount,
            "days_since_delivery": int(raw["days_since_delivery"]),
            "item_condition": str(raw["item_condition"]).strip().lower(),  # UNOPENED -> unopened
            "return_reason": raw.get("return_reason", ""),
            "invoice_available": bool(raw["invoice_available"]),
            "photo_evidence": bool(raw["photo_evidence_available"]),
            "previous_returns_90d": int(raw["previous_returns_90_days"]),
        }
    except KeyError as e:
        raise KeyError(f"Missing field {e} in record: {list(raw.keys())}") from e


# ----------------------------------------------------------------------------
# Deterministic rule checks
# ----------------------------------------------------------------------------
def check_policy(rec: dict) -> list[str]:
    """Rules 1-5. Returns list of failed conditions (empty = all satisfied)."""
    issues = []
    if rec["amount"] >= MAX_AUTO_AMOUNT:
        issues.append(f"Amount Rs.{rec['amount']:,} is not below Rs.{MAX_AUTO_AMOUNT:,}")
    if rec["days_since_delivery"] > MAX_DAYS:
        issues.append(f"Requested {rec['days_since_delivery']} days after delivery (limit {MAX_DAYS})")
    if not rec["invoice_available"]:
        issues.append("Customer invoice not available")
    cond = rec["item_condition"].lower()
    if not (cond == "unopened" or (cond == "damaged" and rec["photo_evidence"])):
        if cond == "damaged":
            issues.append("Item damaged but no supporting photographs")
        else:
            issues.append(f"Item condition '{cond}' is not unopened or documented-damaged")
    if rec["previous_returns_90d"] >= MAX_PREV_RETURNS:
        issues.append(
            f"{rec['previous_returns_90d']} previous returns in 90 days "
            f"(must be fewer than {MAX_PREV_RETURNS})"
        )
    return issues


def parse_risk_level(text: str) -> str:
    for line in text.splitlines():
        if line.strip().upper().startswith("RISK_LEVEL"):
            val = line.split(":", 1)[-1].strip().upper()
            for lvl in ("HIGH", "MEDIUM", "LOW"):
                if lvl in val:
                    return lvl
    return "HIGH"  # fail-safe: unparseable risk output is escalated


# ----------------------------------------------------------------------------
# Executors
# ----------------------------------------------------------------------------
class EligibilityExecutor(Executor):
    """Runs deterministic policy checks, then asks the Eligibility Agent to explain."""

    def __init__(self, agent, id: str = "eligibility"):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def run(self, case: CaseState, ctx: WorkflowContext[CaseState]) -> None:
        case.eligibility_issues = check_policy(case.record)
        prompt = (
            f"Policy:\n{POLICY_TEXT}\n\nRequest:\n{json.dumps(case.record, indent=2)}\n\n"
            f"Deterministic check failures: {case.eligibility_issues or 'None'}\n\n"
            "In 2-4 sentences state whether the request meets eligibility requirements "
            "and explain any exceptions. Do not invent facts."
        )
        result = await self.agent.run(prompt)
        case.eligibility_findings = result.text.strip()
        await ctx.send_message(case)


class RiskExecutor(Executor):
    def __init__(self, agent, id: str = "risk"):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def run(self, case: CaseState, ctx: WorkflowContext[CaseState]) -> None:
        prompt = (
            f"Request:\n{json.dumps(case.record, indent=2)}\n\n"
            "Assess risk: unusual return frequency, missing evidence, high value.\n"
            "Reply in this exact format:\n"
            "RISK_LEVEL: LOW|MEDIUM|HIGH\n"
            "ASSESSMENT: <2-3 sentences>"
        )
        result = await self.agent.run(prompt)
        case.risk_level = parse_risk_level(result.text)
        case.risk_assessment = result.text.strip()
        await ctx.send_message(case)


class ApprovalGateway(Executor):
    """Conditional routing. Auto-approves or pauses for the manager."""

    def __init__(self, id: str = "approval_gateway"):
        super().__init__(id=id)

    @handler
    async def route(self, case: CaseState, ctx: WorkflowContext[CaseState]) -> None:
        issues = list(case.eligibility_issues)
        if case.risk_level == "HIGH":
            issues.append("Risk Agent flagged HIGH risk")

        if not issues:
            case.route = "Automatic"
            case.decision = "AUTO_APPROVED"
            await ctx.send_message(case)
            return

        case.route = "Human Review"
        case.eligibility_issues = issues
        req = ApprovalRequest(
            request_id=case.record["request_id"],
            item=case.record["product"],
            amount=case.record["amount"],
            eligibility_issues=issues,
            risk_assessment=case.risk_assessment,
            case=case,
        )
        # Pauses the workflow until a response is supplied.
        await ctx.request_info(request_data=req, response_type=str)

    @response_handler
    async def on_manager_decision(
        self, original_request: ApprovalRequest, response: str, ctx: WorkflowContext[CaseState]
    ) -> None:
        case = original_request.case  # context preserved
        # Decision is set deterministically in Python; AI cannot override it.
        case.decision = "MANAGER_APPROVED" if response.strip().lower() == "approve" else "MANAGER_REJECTED"
        await ctx.send_message(case)


class CustomerResponseExecutor(Executor):
    def __init__(self, agent, id: str = "customer_response"):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def run(self, case: CaseState, ctx: WorkflowContext[Never, dict]) -> None:
        approved = case.decision in ("AUTO_APPROVED", "MANAGER_APPROVED")
        r = case.record
        prompt = (
            f"Write a short, polite customer message.\n"
            f"Customer request: {r['request_type']} for '{r['product']}' (order {r['order_id']}).\n"
            f"FINAL DECISION (fixed, do not change): {'APPROVED' if approved else 'REJECTED'}.\n"
            + ("Say the request is approved and will proceed to the next processing step. "
               "Do NOT claim any refund or replacement has been completed or issued.\n"
               if approved else
               "Politely say the request could not be approved. Do NOT offer to reverse it. "
               "Do NOT mention internal risk scores.\n")
        )
        result = await self.agent.run(prompt)
        case.customer_message = result.text.strip()

        output = {
            "request_id": r["request_id"],
            "order_id": r["order_id"],
            "product": r["product"],
            "requested_amount": r["amount"],
            "eligibility_findings": {
                "failed_conditions": case.eligibility_issues,
                "summary": case.eligibility_findings,
            },
            "risk_assessment": {"level": case.risk_level, "details": case.risk_assessment},
            "approval_route": case.route,
            "final_decision": case.decision,
            "customer_communication_draft": case.customer_message,
        }
        await ctx.yield_output(output)


# ----------------------------------------------------------------------------
# Workflow construction (works on old and new Agent Framework APIs)
# ----------------------------------------------------------------------------
def build_workflow(elig_agent, risk_agent, resp_agent):
    eligibility = EligibilityExecutor(elig_agent)
    risk = RiskExecutor(risk_agent)
    gateway = ApprovalGateway()
    response = CustomerResponseExecutor(resp_agent)
    try:
        builder = WorkflowBuilder(start_executor=eligibility)        # newer API
    except TypeError:
        builder = WorkflowBuilder().set_start_executor(eligibility)  # older API
    return (
        builder
        .add_edge(eligibility, risk)
        .add_edge(risk, gateway)
        .add_edge(gateway, response)
        .build()
    )


# ----------------------------------------------------------------------------
# Human-in-the-loop input handling
# ----------------------------------------------------------------------------
class ManagerPrompt:
    def __init__(self, scripted: list[str] | None = None):
        self.scripted = list(scripted or [])

    def ask(self, req: ApprovalRequest) -> str:
        print("\n" + "=" * 60)
        print("  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED")
        print("=" * 60)
        print(f"Request ID : {req.request_id}")
        print(f"Item       : {req.item}")
        print(f"Amount     : Rs.{req.amount:,}")
        print("Eligibility issues:")
        for i in req.eligibility_issues:
            print(f"  - {i}")
        print(f"Risk assessment:\n  {req.risk_assessment.replace(chr(10), chr(10) + '  ')}")
        while True:
            if self.scripted:
                ans = self.scripted.pop(0)
                print(f"Enter 'approve' or 'reject': {ans}   (scripted)")
            else:
                ans = input("Enter 'approve' or 'reject': ")
            ans = ans.strip().lower()
            if ans in ("approve", "reject"):
                return ans
            print(f"  Invalid input '{ans}'. Please type exactly 'approve' or 'reject'.")


def _event_type(event) -> str:
    t = getattr(event, "type", None)
    return str(getattr(t, "value", t)) if t else type(event).__name__


def _start_stream(workflow, message):
    if hasattr(workflow, "run_stream"):
        return workflow.run_stream(message)           # older API
    return workflow.run(message, stream=True)         # newer API


def _resume_stream(workflow, responses: dict):
    if hasattr(workflow, "send_responses_streaming"):
        return workflow.send_responses_streaming(responses)   # older API
    return workflow.run(stream=True, responses=responses)     # newer API


async def process_request(workflow, record: dict, manager: ManagerPrompt) -> dict | None:
    final = None
    stream = _start_stream(workflow, CaseState(record=record))
    while True:
        pending: dict[str, ApprovalRequest] = {}
        async for event in stream:
            et = _event_type(event)
            if et in ("request_info", "RequestInfoEvent"):
                pending[event.request_id] = event.data
            elif et in ("output", "WorkflowOutputEvent"):
                final = event.data
        if not pending:
            break
        responses = {rid: manager.ask(data) for rid, data in pending.items()}
        print("Resuming workflow with manager decision...")
        stream = _resume_stream(workflow, responses)
    return final


# ----------------------------------------------------------------------------
# Config + client/agent helpers
# ----------------------------------------------------------------------------
def check_config() -> None:
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        print("ERROR: Missing Azure OpenAI configuration: " + ", ".join(missing))
        print("Copy .env.example to .env and fill in the values.")
        sys.exit(1)


def make_client():
    """Let the framework read AZURE_OPENAI_API_KEY / _BASE_URL / _MODEL from the environment."""
    candidates = []
    try:
        from agent_framework.openai import OpenAIChatClient
        candidates.append(lambda: OpenAIChatClient())
    except ImportError:
        pass
    try:
        from agent_framework.azure import AzureOpenAIChatClient
        candidates.append(lambda: AzureOpenAIChatClient())
    except ImportError:
        pass

    last_err = None
    for build in candidates:
        try:
            return build()
        except Exception as e:  # wrong settings for this client, try the next
            last_err = e
    print(f"ERROR: Could not create the Azure OpenAI client: {last_err}")
    sys.exit(1)


def make_agent(client, name: str, instructions: str):
    """Newer versions use as_agent, older ones create_agent."""
    factory = getattr(client, "as_agent", None) or getattr(client, "create_agent")
    return factory(name=name, instructions=instructions)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
async def main(args) -> None:
    load_dotenv()
    check_config()

    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if isinstance(raw, dict):  # handle {"requests": [...]} style files
        raw = next(v for v in raw.values() if isinstance(v, list))
    records = [normalize_record(r) for r in raw]
    print(f"Loaded {len(records)} return requests from {args.input}")

    scripted = [s.strip() for s in args.scripted.split(",")] if args.scripted else None
    manager = ManagerPrompt(scripted)

    client = make_client()

    elig_agent = make_agent(
        client,
        "EligibilityAgent",
        "You review e-commerce return requests against the supplied return policy "
        "and explain eligibility and exceptions concisely and factually.",
    )
    risk_agent = make_agent(
        client,
        "RiskAgent",
        "You are a fraud/risk analyst for returns. Be concise. "
        "Always follow the requested output format exactly.",
    )
    resp_agent = make_agent(
        client,
        "CustomerResponseAgent",
        "You write polite customer-facing messages. Never claim a refund or "
        "replacement has been completed. Never contradict the given final decision.",
    )

    results = []
    for rec in records:
        print(f"\n--- Processing {rec['request_id']} ({rec['product']}) ---")
        workflow = build_workflow(elig_agent, risk_agent, resp_agent)  # fresh run per request
        out = await process_request(workflow, rec, manager)
        if out:
            results.append(out)
            print(f"[{out['request_id']}] route={out['approval_route']} decision={out['final_decision']}")

    Path("final_output.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n===== FINAL STRUCTURED OUTPUT =====")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("\nSummary:")
    for r in results:
        print(f"  {r['request_id']}: {r['approval_route']:<12} -> {r['final_decision']}")
    print("\n(Simulation only: no payments, messages, or replacements were executed.)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="returns.json")
    p.add_argument(
        "--scripted",
        default="",
        help="Comma-separated manager inputs for demo, e.g. 'maybe,approve,reject'",
    )
    asyncio.run(main(p.parse_args()))