============================================================
MICROSOFT AGENT FRAMEWORK
IT INCIDENT ROUTING SYSTEM
Authentication: Azure Foundry API Key
============================================================

Azure Foundry configuration loaded.
Endpoint: https://day29foundrypractice.openai.azure.com/openai/v1
Deployment: gpt-4.1-mini

Total incidents loaded: 4

Azure Foundry client initialized.
Graph workflow built successfully.

============================================================
Processing Incident: INC101
Description: The corporate email service is unavailable for every employee across the company.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC101
Severity: HIGH
Assigned Agent: EscalationAgent

1. Incident summary:  
Corporate email service is down company-wide, impacting all employees' communication and productivity.

2. Responsible support team:  
Email Infrastructure and Messaging Support Team.

3. Immediate containment actions:  
- Verify email server status and connectivity.  
- Check for recent changes or alerts affecting email systems.  
- Redirect users to alternative communication channels if available (e.g., instant messaging or phone).

4. Escalation procedure:  
- Notify Email Infrastructure Lead immediately.  
- Escalate to Network Operations if connectivity issues are identified.  
- Engage vendor support for email platform if internal troubleshooting fails within 15 minutes.  
- Alert Senior IT management for business impact awareness.

5. Communication recommendations:  
- Send a company-wide notification explaining the issue and estimated resolution time.  
- Provide regular status updates every 30 minutes.  
- Notify key business units and executives directly via alternative communication tools.  
- Confirm resolution and send a post-incident report once service is restored.
------------------------------------------------------------

============================================================
Processing Incident: INC102
Description: One employee's wireless mouse stopped working.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC102
Severity: LOW
Assigned Agent: ResolutionAgent

Here are some simple steps to troubleshoot your wireless mouse:

1. **Check the Batteries:** Make sure the mouse has fresh batteries and they are inserted correctly. Replace them if needed.
2. **Turn the Mouse Off and On:** Switch the mouse off, wait a few seconds, then turn it back on to reset the connection.
3. **Check the USB Receiver:** Ensure the wireless USB receiver is securely plugged into your computer. Try unplugging and plugging it back in.
4. **Reconnect the Mouse:** If your mouse has a connect button, press it to re-pair with the USB receiver.
5. **Try Another USB Port:** Plug the USB receiver into a different USB port on your computer to rule out a port issue.

**When to contact the help desk:**  
If these steps don’t restore the mouse function, or if the mouse still won’t connect or respond, please contact the help desk for further assistance.
------------------------------------------------------------

============================================================
Processing Incident: INC103
Description: The company-wide payment processing system is down and transactions are failing.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC103
Severity: HIGH
Assigned Agent: EscalationAgent

1. Incident summary: Company-wide payment processing system is down, causing transaction failures and blocking all payment activities.

2. Responsible support team: Payment Systems Support Team and Infrastructure Operations Team.

3. Immediate containment actions:  
- Confirm the outage scope and impact.  
- Redirect payment requests to backup or alternate processing systems if available.  
- Notify relevant business units to halt payment-dependent operations to prevent data corruption.

4. Escalation procedure:  
- Immediately escalate to Payment Systems Lead and IT Operations Manager.  
- Engage third-level support or vendor specialists for critical payment platform components.  
- Escalate to CISO if there is suspicion of security breach or data compromise.

5. Communication recommendations:  
- Inform executive leadership and impacted business units with clear status updates every 30 minutes.  
- Provide estimated time to resolution if known, or timeline for next update.  
- Prepare holding statement for external customers or partners as applicable.
------------------------------------------------------------

============================================================
Processing Incident: INC104
Description: One employee cannot print to the nearby office printer.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC104
Severity: LOW
Assigned Agent: ResolutionAgent

Here are some simple troubleshooting steps you can follow if you cannot print to the nearby office printer:

1. Make sure the printer is turned on and connected to the power source.
2. Check that the printer is connected to the network or directly to your computer.
3. Verify that you have selected the correct printer when printing your document.
4. Ensure there is enough paper and ink or toner in the printer.
5. Restart your computer and try printing again.

If you still cannot print after trying these steps, please contact the help desk for further assistance. They can check for network or printer settings issues that might need deeper troubleshooting.
------------------------------------------------------------

============================================================
ALL INCIDENTS PROCESSED
============================================================




Vendor_approval_workflow


============================================================
REQUEST PR101: Office chairs
  ProcurementAgent: checking justification
  RiskAgent: assessing purchase
  RiskAgent: LOW
  ApprovalGateway: automatic approval
  SummaryAgent: preparing decision record

FINAL RECORD
PR101 -> AUTO_APPROVED
Procurement Decision Record (Demo)

Request ID: PR101  
Item: Office chairs  
Vendor: Cedar Office Supplies (approved)  
Quantity: 8  
Amount: INR 32,000  
Risk Level: LOW  
Decision: AUTO_APPROVED  
Decision By: Demo approval policy  

Next Steps: Proceed to initiate purchase order creation with Cedar Office Supplies to replace damaged chairs in the customer support area. This record is a demo and does not constitute a placed order.

============================================================
REQUEST PR102: Developer laptops
  ProcurementAgent: checking justification
  RiskAgent: assessing purchase
  RiskAgent: LOW
  ApprovalGateway: PAUSED - awaiting manager

==================================================
MANAGER APPROVAL REQUIRED
Review PR102 | Developer laptops | INR 1,250,000 | Risk: LOW
Procurement review: The request to replace 20 aging developer laptops is justified to maintain team productivity and ensure up-to-date hardware for efficient software development. The approved vendor, Orion Computing, aligns with procurement policy, supporting a smooth purchase process.
Type approve or reject: approve
  SummaryAgent: preparing decision record

FINAL RECORD
PR102 -> MANAGER_APPROVED
Procurement Decision Record (Demo)

Request ID: PR102  
Item: Developer laptops  
Vendor: Orion Computing  
Amount: INR 1,250,000  
Risk Level: LOW  
Decision: MANAGER_APPROVED  
Decision Type: Human manager

Next Steps: Proceed with finalizing purchase orders, coordinate with Orion Computing for delivery timelines, and prepare for asset deployment to the development team.  

Note: This is a demo record and does not represent a placed order.

============================================================
REQUEST PR103: Printer cartridges
  ProcurementAgent: checking justification
  RiskAgent: assessing purchase
  RiskAgent: LOW
  ApprovalGateway: automatic approval
  SummaryAgent: preparing decision record

FINAL RECORD
PR103 -> AUTO_APPROVED
Procurement Decision Record - Demo

Request ID: PR103  
Item: Printer cartridges  
Vendor: Cedar Office Supplies (approved)  
Quantity: 10  
Amount: INR 8,500  
Risk Level: LOW  
Decision: AUTO_APPROVED  
Decision By: Demo approval policy  

Next Steps: Proceed with order placement from Cedar Office Supplies to replenish printer cartridges ensuring uninterrupted monthly operations. This is a demo record; no actual order has been placed.

============================================================
REQUEST PR104: Network infrastructure upgrade
  ProcurementAgent: checking justification
  RiskAgent: assessing purchase
  RiskAgent: HIGH
  ApprovalGateway: PAUSED - awaiting manager

==================================================
MANAGER APPROVAL REQUIRED
Review PR104 | Network infrastructure upgrade | INR 480,000 | Risk: HIGH
Procurement review: The purchase request for upgrading access switches with Newline Networks is justified to support the expanded office capacity, ensuring adequate network performance and scalability. As this is a first-time vendor, due diligence on vendor reliability and post-purchase support is recommended before approval.
Type approve or reject: reject
  SummaryAgent: preparing decision record

FINAL RECORD
PR104 -> MANAGER_REJECTED
Procurement Decision Record (Demo)

Request ID: PR104  
Amount: INR 480,000  
Risk Level: HIGH  
Decision: MANAGER_REJECTED  
Decision By: Human manager  

Summary: The purchase request for network infrastructure upgrade with Newline Networks, a new vendor, was rejected by the human manager due to high risk concerns despite the justification.  

Next Steps: Conduct further due diligence on vendor reliability and post-purchase support before reconsideration. No order has been placed.


