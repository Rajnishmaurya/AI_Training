# E-commerce Returns & Refund Processing: Multi-Agent Workflow

A graph-based multi-agent application built with **Microsoft Agent Framework** and **Azure OpenAI** (Python). It automates the first review of customer return, refund and replacement requests, and pauses for a human manager when a request is high-value, risky or exceptional.

> **Simulation only.** No payments are processed, no messages are sent and no replacements are initiated.

---

## Workflow

```
Return Request -> Eligibility Executor -> Risk Executor -> Approval Gateway
               -> Customer Response Executor -> Final Output
```

| Executor | Type | Responsibility |
|---|---|---|
| **EligibilityExecutor** | Python + AI agent | Runs the deterministic policy checks in Python, then the Eligibility Agent explains the findings and exceptions. |
| **RiskExecutor** | AI agent | The Risk Agent returns `RISK_LEVEL` (LOW / MEDIUM / HIGH) and a short assessment. Unparseable output is treated as HIGH (fail-safe). |
| **ApprovalGateway** | Python | Conditional routing. If every rule passes, the request is `AUTO_APPROVED`. Otherwise it pauses the workflow with `ctx.request_info(...)` and waits for a manager. |
| **CustomerResponseExecutor** | AI agent | Writes the customer message from the already-fixed decision and yields the structured final output. |

### Business rules (deterministic Python)

A request is automatically approved only if **all** of these hold:

1. Product amount is below Rs.25,000.
2. The request is within 30 days of delivery.
3. A customer invoice is available.
4. The item is unopened, or damaged with supporting photographs.
5. The customer has fewer than 3 previous returns in 90 days.
6. The Risk Agent has not flagged a HIGH-risk concern.

If any condition fails, the request is escalated for human review.

### Human-in-the-loop

- The `ApprovalGateway` calls `ctx.request_info(...)`, which **pauses** the workflow.
- The console shows the request ID, item, amount, eligibility issues and risk assessment.
- The manager types `approve` or `reject`. Any other input is rejected and re-prompted.
- The answer **resumes** the workflow, and a `@response_handler` sets `MANAGER_APPROVED` or `MANAGER_REJECTED`.
- The request context travels inside the approval request payload, so nothing is lost across the pause.
- The decision is set in Python, and the Customer Response Agent only receives the final decision as a fixed input. **The AI cannot override a human rejection.**

### Final output (per request)

Request ID and order ID, product and requested amount, eligibility findings, risk assessment, approval route (`Automatic` or `Human Review`), final decision (`AUTO_APPROVED`, `MANAGER_APPROVED` or `MANAGER_REJECTED`) and the customer communication draft. Results are printed and saved to `final_output.json`.

---

## Project files

| File | Purpose |
|---|---|
| `returns_workflow.py` | Complete application |
| `returns.json` | Input data (10 customer requests) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template (no real credentials) |
| `README.md` | This document |

---

## Setup

1. **Create a virtual environment**
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```
2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Configure credentials**: copy `.env.example` to `.env` and fill in your values.
   ```
   AZURE_OPENAI_API_KEY=<your-api-key>
   AZURE_OPENAI_BASE_URL=<your-azure-openai-endpoint>
   AZURE_OPENAI_MODEL=<your-deployment-name>
   ```
   `AZURE_OPENAI_MODEL` must be the **deployment name** from Azure.
   Never commit your real `.env` file. Add it to `.gitignore`.

---

## Run

Interactive (you act as the manager):

```
python returns_workflow.py
```

Demo with scripted manager answers (the first one is invalid on purpose):

```
python returns_workflow.py --scripted "maybe,approve,reject"
```

Custom input file:

```
python returns_workflow.py --input returns.json
```

---

## Testing the workflow

Run against all 10 records in `returns.json` and confirm:

| Scenario | Expected |
|---|---|
| At least two automatic approvals | Route `Automatic`, decision `AUTO_APPROVED` |
| A request paused, then approved | Route `Human Review`, decision `MANAGER_APPROVED` |
| A different request paused, then rejected | Route `Human Review`, decision `MANAGER_REJECTED` |
| Correct resumption | Output appears after "Resuming workflow with manager decision..." with the same request ID |
| Invalid approval input | Message `Invalid input ... Please type exactly 'approve' or 'reject'`, then re-prompt |
| Missing API configuration | Rename or empty `.env` and run. The app lists the missing variables and exits with code 1 |

---

## Error handling

- **Missing configuration:** a clear error naming the missing variables, then exit.
- **Invalid manager input:** re-prompted until `approve` or `reject` is entered.
- **Unparseable risk output:** treated as HIGH risk, so the request is escalated rather than auto-approved.

---

## Screenshots / console output

Add screenshots or pasted console output here showing:

1. An automatic approval
2. A human approval
3. A human rejection

---

## Notes

- Microsoft Agent Framework is in rapid development. This project was run with `agent-framework` 1.25.0. If you use a different version, the event and API names may differ.
- All AI output (eligibility explanation, risk assessment, customer message) is advisory. The routing and final decisions are made by deterministic Python code and the human manager.





=================================================================================================
                                            OUTPUT
=================================================================================================

Loaded 10 return requests from returns.json

--- Processing RET201 (Wireless Keyboard) ---
[RET201] route=Automatic decision=AUTO_APPROVED

--- Processing RET202 (Gaming Laptop) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET202
Item       : Gaming Laptop
Amount     : Rs.79,999
Eligibility issues:
  - Amount Rs.79,999 is not below Rs.25,000
  - Item condition 'used' is not unopened or documented-damaged
Risk assessment:
  RISK_LEVEL: LOW  
  ASSESSMENT: The return request for a high-value item is within a reasonable time frame and includes both invoice and photo evidence. There is no unusual return frequency, and the item condition and reason are plausible. Overall, the risk of fraud appears low.
Enter 'approve' or 'reject': approve
Resuming workflow with manager decision...
[RET202] route=Human Review decision=MANAGER_APPROVED

--- Processing RET203 (Ceramic Dinner Set) ---
[RET203] route=Automatic decision=AUTO_APPROVED

--- Processing RET204 (Travel Suitcase) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET204
Item       : Travel Suitcase
Amount     : Rs.4,599
Eligibility issues:
  - Item damaged but no supporting photographs
Risk assessment:
  RISK_LEVEL: MEDIUM  
  ASSESSMENT: The return is for a high-value item reported as damaged, but no photo evidence was provided, increasing verification difficulty. However, the customer has no previous returns in the last 90 days and the request is made shortly after delivery, reducing suspicion of abuse.
Enter 'approve' or 'reject': apprive
  Invalid input 'apprive'. Please type exactly 'approve' or 'reject'.
Enter 'approve' or 'reject': approve
Resuming workflow with manager decision...
[RET204] route=Human Review decision=MANAGER_APPROVED

--- Processing RET205 (Yoga Mat) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET205
Item       : Yoga Mat
Amount     : Rs.1,999
Eligibility issues:
  - Requested 44 days after delivery (limit 30)
Risk assessment:
  RISK_LEVEL: LOW  
  ASSESSMENT: The return request is low risk as there is no unusual return frequency, the item is unopened, and an invoice is available. The item value is moderate, and the reason given is plausible, with no missing critical evidence for this type of return.
Enter 'approve' or 'reject': approve
Resuming workflow with manager decision...
[RET205] route=Human Review decision=MANAGER_APPROVED

--- Processing RET206 (Desk Lamp) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET206
Item       : Desk Lamp
Amount     : Rs.3,299
Eligibility issues:
  - 4 previous returns in 90 days (must be fewer than 3)
Risk assessment:
  RISK_LEVEL: MEDIUM  
  ASSESSMENT: The return request is for a relatively high-value item and the customer has a high frequency of returns within 90 days, which raises some concern. However, the return is within a reasonable timeframe, unopened, with invoice and photo evidence provided, reducing the overall risk.
Enter 'approve' or 'reject': reject
Resuming workflow with manager decision...
[RET206] route=Human Review decision=MANAGER_REJECTED

--- Processing RET207 (Coffee Grinder) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET207
Item       : Coffee Grinder
Amount     : Rs.6,999
Eligibility issues:
  - Customer invoice not available
Risk assessment:
  RISK_LEVEL: MEDIUM  
  ASSESSMENT: The return request is for a relatively high-value item without invoice or photo evidence, which raises moderate suspicion. However, the unopened condition and lack of previous returns reduce risk slightly. The reason "Received duplicate gift" is plausible but unverifiable.
Enter 'approve' or 'reject': reject
Resuming workflow with manager decision...
[RET207] route=Human Review decision=MANAGER_REJECTED

--- Processing RET208 (Sketchbook Set) ---
[RET208] route=Automatic decision=AUTO_APPROVED

--- Processing RET209 (Smartwatch) ---

============================================================
  WORKFLOW PAUSED - MANAGER APPROVAL REQUIRED
============================================================
Request ID : RET209
Item       : Smartwatch
Amount     : Rs.18,900
Eligibility issues:
  - Item condition 'used' is not unopened or documented-damaged
Risk assessment:
  RISK_LEVEL: LOW  
  ASSESSMENT: The return frequency is low with no previous returns in the last 90 days. Both invoice and photo evidence are provided, supporting the legitimacy of the claim. Despite the high value, the used condition and stated battery issue align with a reasonable refund request.
Enter 'approve' or 'reject': approve
Resuming workflow with manager decision...
[RET209] route=Human Review decision=MANAGER_APPROVED

--- Processing RET210 (Floor Mirror) ---
[RET210] route=Automatic decision=AUTO_APPROVED

===== FINAL STRUCTURED OUTPUT =====
[
  {
    "request_id": "RET201",
    "order_id": "ORD-7301",
    "product": "Wireless Keyboard",
    "requested_amount": 1499,
    "eligibility_findings": {
      "failed_conditions": [],
      "summary": "The return request RET201 meets all eligibility requirements for automatic approval: the product amount is below Rs.25,000, the request is within 30 days of delivery, the invoice is available, the item is unopened, there are no previous returns in the last 90 days, and no high-risk concern is indicated. Therefore, this return can be approved automatically without escalation."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return request is within a reasonable timeframe and for a non-defective unopened item, with no previous returns in the last 90 days. The amount is moderate, and the return reason is legitimate. Missing photo evidence is acceptable given the item is unopened and invoice is available."
    },
    "approval_route": "Automatic",
    "final_decision": "AUTO_APPROVED",
    "customer_communication_draft": "Dear Customer,\n\nWe are pleased to inform you that your refund request for the Wireless Keyboard (order ORD-7301) has been approved. We will now proceed to the next step in processing your request.\n\nThank you for your patience and understanding.\n\nBest regards,  \nCustomer Service Team"
  },
  {
    "request_id": "RET202",
    "order_id": "ORD-7302",
    "product": "Gaming Laptop",
    "requested_amount": 79999,
    "eligibility_findings": {
      "failed_conditions": [
        "Amount Rs.79,999 is not below Rs.25,000",
        "Item condition 'used' is not unopened or documented-damaged"
      ],
      "summary": "The return request does not meet the automatic approval criteria because the product amount of Rs.79,999 exceeds the Rs.25,000 limit, and the item is used rather than unopened or documented as damaged. Therefore, this request must be escalated for human review."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return request for a high-value item is within a reasonable time frame and includes both invoice and photo evidence. There is no unusual return frequency, and the item condition and reason are plausible. Overall, the risk of fraud appears low."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_APPROVED",
    "customer_communication_draft": "Dear Customer, \n\nWe are pleased to inform you that your refund request for the Gaming Laptop (order ORD-7302) has been approved. We will now proceed to the next step in the processing. \n\nThank you for your patience and understanding.  \n\nBest regards,  \n[Your Company Name]"
  },
  {
    "request_id": "RET203",
    "order_id": "ORD-7303",
    "product": "Ceramic Dinner Set",
    "requested_amount": 2499,
    "eligibility_findings": {
      "failed_conditions": [],
      "summary": "The return request RET203 meets all eligibility requirements for automatic approval: the product amount is below Rs. 25,000, the request is within 30 days of delivery, the invoice is available, the item is damaged with photo evidence, and the customer has fewer than 3 previous returns in the last 90 days. There is no mention of any HIGH-risk concern by the Risk Agent. Therefore, this replacement request is automatically approved."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return request is for a damaged item within a reasonable timeframe (9 days), with photo evidence and an available invoice. The customer has only one previous return in the last 90 days, and the item value is moderate, indicating low risk."
    },
    "approval_route": "Automatic",
    "final_decision": "AUTO_APPROVED",
    "customer_communication_draft": "Dear Customer,\n\nThank you for contacting us regarding your Ceramic Dinner Set (order ORD-7303). We are pleased to inform you that your replacement request has been approved and will now proceed to the next processing step.\n\nWe appreciate your patience and will keep you informed of any updates.\n\nBest regards,  \n[Your Company Name] Customer Service Team"
  },
  {
    "request_id": "RET204",
    "order_id": "ORD-7304",
    "product": "Travel Suitcase",
    "requested_amount": 4599,
    "eligibility_findings": {
      "failed_conditions": [
        "Item damaged but no supporting photographs"
      ],
      "summary": "The return request RET204 does not meet the eligibility requirements for automatic approval because the item is damaged but no supporting photographs have been provided, which violates condition 4. Although the amount, days since delivery, invoice availability, and previous returns meet the policy criteria, the lack of photo evidence requires this request to be escalated for human review."
    },
    "risk_assessment": {
      "level": "MEDIUM",
      "details": "RISK_LEVEL: MEDIUM  \nASSESSMENT: The return is for a high-value item reported as damaged, but no photo evidence was provided, increasing verification difficulty. However, the customer has no previous returns in the last 90 days and the request is made shortly after delivery, reducing suspicion of abuse."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_APPROVED",
    "customer_communication_draft": "Dear Customer,\n\nThank you for contacting us regarding your order ORD-7304. We are pleased to inform you that your refund request for the Travel Suitcase has been approved and will proceed to the next processing step.\n\nWe appreciate your patience and will keep you updated on the progress.\n\nBest regards,  \nCustomer Service Team"
  },
  {
    "request_id": "RET205",
    "order_id": "ORD-7305",
    "product": "Yoga Mat",
    "requested_amount": 1999,
    "eligibility_findings": {
      "failed_conditions": [
        "Requested 44 days after delivery (limit 30)"
      ],
      "summary": "The return request RET205 does not meet the eligibility requirements because it was made 44 days after delivery, exceeding the 30-day limit specified in the policy. Although the product amount, invoice availability, item condition, and previous returns meet the criteria, the delayed request requires escalation for human review."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return request is low risk as there is no unusual return frequency, the item is unopened, and an invoice is available. The item value is moderate, and the reason given is plausible, with no missing critical evidence for this type of return."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_APPROVED",
    "customer_communication_draft": "Dear Customer, \n\nWe are pleased to inform you that your refund request for the Yoga Mat (order ORD-7305) has been approved. We will now proceed to the next step in the processing. \n\nThank you for your patience and understanding. \n\nBest regards,  \n[Your Company Name] Customer Support"
  },
  {
    "request_id": "RET206",
    "order_id": "ORD-7306",
    "product": "Desk Lamp",
    "requested_amount": 3299,
    "eligibility_findings": {
      "failed_conditions": [
        "4 previous returns in 90 days (must be fewer than 3)"
      ],
      "summary": "The return request RET206 does not meet the eligibility requirements due to exceeding the allowed number of previous returns in the last 90 days, with 4 returns instead of fewer than 3. All other criteria, including amount, request timing, invoice availability, item condition, and photo evidence, are satisfied. Therefore, this request must be escalated for human review."
    },
    "risk_assessment": {
      "level": "MEDIUM",
      "details": "RISK_LEVEL: MEDIUM  \nASSESSMENT: The return request is for a relatively high-value item and the customer has a high frequency of returns within 90 days, which raises some concern. However, the return is within a reasonable timeframe, unopened, with invoice and photo evidence provided, reducing the overall risk."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_REJECTED",
    "customer_communication_draft": "Dear Customer,\n\nThank you for reaching out regarding your Desk Lamp from order ORD-7306. After careful consideration, we are unable to approve your replacement request. \n\nWe appreciate your understanding and are here to assist with any other questions you may have.\n\nBest regards,  \n[Your Company Name] Customer Support Team"
  },
  {
    "request_id": "RET207",
    "order_id": "ORD-7307",
    "product": "Coffee Grinder",
    "requested_amount": 6999,
    "eligibility_findings": {
      "failed_conditions": [
        "Customer invoice not available"
      ],
      "summary": "The return request RET207 does not meet the eligibility requirements because the customer invoice is not available, which is mandatory for automatic approval. Although the product amount is below Rs. 25,000, the request is within 30 days, the item is unopened, and there are no previous returns, the lack of an invoice means this request must be escalated for human review."
    },
    "risk_assessment": {
      "level": "MEDIUM",
      "details": "RISK_LEVEL: MEDIUM  \nASSESSMENT: The return request is for a relatively high-value item without invoice or photo evidence, which raises moderate suspicion. However, the unopened condition and lack of previous returns reduce risk slightly. The reason \"Received duplicate gift\" is plausible but unverifiable."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_REJECTED",
    "customer_communication_draft": "Dear Customer,\n\nThank you for reaching out regarding your order ORD-7307. After careful consideration, we are unable to approve your refund request for the Coffee Grinder. \n\nWe appreciate your understanding and are here to assist with any other questions you may have.\n\nBest regards,  \nCustomer Support Team"
  },
  {
    "request_id": "RET208",
    "order_id": "ORD-7308",
    "product": "Sketchbook Set",
    "requested_amount": 1099,
    "eligibility_findings": {
      "failed_conditions": [],
      "summary": "The return request RET208 for the Sketchbook Set meets all the eligibility requirements for automatic approval: the amount is below Rs.25,000, the request is within 30 days of delivery, the invoice is available, the item is unopened, and there is only 1 previous return in the last 90 days. There is no mention of a HIGH-risk concern, so this request is eligible for automatic approval."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The customer has one previous return in the last 90 days, which is not excessive. The item is unopened with invoice provided, and the return amount is moderate. No photo evidence is required given the return reason and condition, so risk is low."
    },
    "approval_route": "Automatic",
    "final_decision": "AUTO_APPROVED",
    "customer_communication_draft": "Dear Customer,  \n\nWe are pleased to inform you that your refund request for the 'Sketchbook Set' (order ORD-7308) has been approved. We will now proceed to the next step in the processing.  \n\nThank you for your patience and understanding.  \n\nBest regards,  \nCustomer Support Team"
  },
  {
    "request_id": "RET209",
    "order_id": "ORD-7309",
    "product": "Smartwatch",
    "requested_amount": 18900,
    "eligibility_findings": {
      "failed_conditions": [
        "Item condition 'used' is not unopened or documented-damaged"
      ],
      "summary": "The return request RET209 does not meet the eligibility requirements for automatic approval because the item condition is \"used,\" which does not satisfy the policy condition that the item must be unopened or damaged with supporting photographs. Despite meeting all other criteria, this exception requires escalation for human review."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return frequency is low with no previous returns in the last 90 days. Both invoice and photo evidence are provided, supporting the legitimacy of the claim. Despite the high value, the used condition and stated battery issue align with a reasonable refund request."
    },
    "approval_route": "Human Review",
    "final_decision": "MANAGER_APPROVED",
    "customer_communication_draft": "Dear Customer, \n\nWe are pleased to inform you that your refund request for the Smartwatch (order ORD-7309) has been approved. We will now proceed to the next step in the processing. \n\nThank you for your patience and understanding. \n\nBest regards,  \n[Your Company Name]"
  },
  {
    "request_id": "RET210",
    "order_id": "ORD-7310",
    "product": "Floor Mirror",
    "requested_amount": 12500,
    "eligibility_findings": {
      "failed_conditions": [],
      "summary": "The return request RET210 for the Floor Mirror meets all automatic approval criteria: the amount is below Rs.25,000, the request is made within 30 days, the invoice is available, the item is damaged with photo evidence, there are no previous returns in the last 90 days, and no high-risk concerns are noted. Therefore, this replacement request is eligible for automatic approval under the return policy."
    },
    "risk_assessment": {
      "level": "LOW",
      "details": "RISK_LEVEL: LOW  \nASSESSMENT: The return request appears legitimate with invoice and photo evidence provided. The customer has no unusual return frequency and the reason given matches the item condition. Despite the relatively high value, the evidence supports approval."
    },
    "approval_route": "Automatic",
    "final_decision": "AUTO_APPROVED",
    "customer_communication_draft": "Dear Customer, \n\nThank you for reaching out regarding your Floor Mirror (order ORD-7310). Your replacement request has been approved and will now proceed to the next processing step. \n\nWe appreciate your patience and will keep you informed of any updates.  \n\nBest regards,  \n[Your Company Name]"
  }
]

Summary:
  RET201: Automatic    -> AUTO_APPROVED
  RET202: Human Review -> MANAGER_APPROVED
  RET203: Automatic    -> AUTO_APPROVED
  RET204: Human Review -> MANAGER_APPROVED
  RET205: Human Review -> MANAGER_APPROVED
  RET206: Human Review -> MANAGER_REJECTED
  RET207: Human Review -> MANAGER_REJECTED
  RET208: Automatic    -> AUTO_APPROVED
  RET209: Human Review -> MANAGER_APPROVED
  RET210: Automatic    -> AUTO_APPROVED

(Simulation only: no payments, messages, or replacements were executed.)