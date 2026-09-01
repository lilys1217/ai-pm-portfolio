"""Day 2: structured triage - schema-guaranteed JSON + client-side validation."""
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel
import anthropic

from exceptions import EXCEPTIONS, NON_BILLING_EXCEPTIONS

load_dotenv()
client = anthropic.Anthropic()

# --- 1. The contract: the shape every triage result MUST have ---
TRIAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [
                "High Bill Complaint",
                "Estimated Read Streak",
                "Rate Code Mismatch",
                "Net Metering True-Up",
                "Meter Read Anomaly",
                "Other / Needs Human Review"
            ],
        },
        "priority": {"type": "string", "enum": ["P1", "P2", "P3"]},
        "routing": {
            "type": "string",
            "enum": ["CSR Callback", "Billing Analyst", "Field Service Order"],
        },
        "rationale": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    },
    "required": ["category", "priority", "routing", "rationale","confidence"],
    "additionalProperties": False,
}

# --- 2. The same contract client-side, as a Pydantic model ---
class TriageResult(BaseModel):
    category: Literal[
        "High Bill Complaint",
        "Estimated Read Streak",
        "Rate Code Mismatch",
        "Net Metering True-Up",
        "Meter Read Anomaly",
        "Other / Needs Human Review"
    ]
    priority: Literal["P1", "P2", "P3"]
    routing: Literal["CSR Callback", "Billing Analyst", "Field Service Order"]
    rationale: str
    confidence: Literal["high", "medium", "low"]


def triage(exception_text: str) -> TriageResult:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=(
            """
            You are a billing-exception triage assistant for an electric cooperative. Base the rationale only on data present in the exception.
            <category_definitions>
            - High Bill Complaint: the dollar amount is unexpectedly high while the read sequence
            and usage are internally consistent with each other. Decisive signal: reads and usage
            look normal, the bill does not. The meter is NOT implicated.
            
            - Meter Read Anomaly: the read sequence itself is implausible - rollbacks, spikes
            inconsistent with history, stuck registers - independent of the dollar amount.
            Decisive signal: the reads, not the bill, are what looks wrong.

            - Estimated Read Streak: Estimated Read Streak: The current month’s estimated kWh usage
            is at least 20% higher than the previous month’s estimated or utility-recorded kWh usage. 
            Decisive Signal: Both the current month’s billed amount and kWh usage have increased by at 
            least 20% compared with the previous month, with no rate change that would otherwise explain 
            the increase.
            
            - Rate Code Mismatch: Rate Code Mismatch: The rate code shown on the current bill does not 
            match the rate code in the customer’s latest rate assignment history record. 
            Decisive Signal: The rate code on the current bill has changed, while the customer 
            reports that they neither requested a rate change nor received notification of one.
            
            - Net Metering True-Up: Net Metering True-Up: The account has active net metering status, 
            but the current bill shows no generated kWh and no generation credit. Decisive Signal: The 
            account’s net metering status is active, while both generated kWh and generation credit on 
            the current bill are zero.
            
            - Other / Needs Human Review: not a billing matter (outages, field damage, service
            requests), OR the fields contradict each other.
            </category_definitions>

            <priority_rules>
            - P1: the member is currently without service or facing disconnection.
            - P2: the member is facing billing calculation issue, meter reading issue, 
            or billing rate issue with no service risk
            - P3: the member is complaining about not receiving the bill, new service inquiry, 
            bill calculation explanation, related to inquiry or improvement feedback 
            </priority_rules>

            <confidence_rules>
            - Report confidence honestly. Contradictory or missing evidence means "low", never "high".
            - If the exception does not clearly fit a billing category, or its fields contradict
            each other, use "Other / Needs Human Review".
            </confidence_rules>

            <rationale_rules>
            - The rationale must be a single sentence that cites specific data fields from the exception.
            </rationale_rules>

            <examples>
            <example>
            <exception>
            Acct 30817: residential, rate R-1. Bill $612 vs 12-month average $190. Reads: 44,120 -> 46,220 (2,100 kWh), 
            both actual reads; 12-month average usage 780 kWh. No rate change on account. Member called 8/14 stating nothing has changed.
            </exception>
            <output>
            {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", "rationale": "Both reads are actual 
            and the 2,100 kWh matches the billed usage, but the usage is inconsistent compared to history usage awill need a technical 
            resource to check out at the field is reading is incorrect", "confidence": "high"}
            </output>
            </example>

            <example>
            <exception>
            Acct 51290: residential, rate R-1. Net metering account. Account has no generation or interconnection record on net meter status history table. 
            Reads: 12,300 -> 13,050 (750 kWh), matching the 12-month average. Bill $186, normal for the rate class.
            </exception>
            <output>
            {"category": "Net Metering True-Up", "priority": "P2", "routing": "Field Service Order", "rationale": "The Net Metering 
            True-Up flag contradicts the absence of any generation record, will need field service to check if the net meter is up and working properly.", "confidence": "medium"}
            </output>
            </example>
            </examples>

            """
        ),
        messages=[
            {"role": "user", "content": f"Triage this exception:\n\n{exception_text}"}
        ],
        output_config={
            "format": {"type": "json_schema", "schema": TRIAGE_SCHEMA}
        },
    )
    raw = resp.content[0].text  # guaranteed valid JSON matching the schema
    return TriageResult.model_validate_json(raw)

if __name__ == "__main__":
    for i, exc in enumerate(EXCEPTIONS + NON_BILLING_EXCEPTIONS, 1):
        r = triage(exc)
        print(f"===== Exception {i} =====")
        print(f"  category : {r.category}")
        print(f"  priority : {r.priority}")
        print(f"  routing  : {r.routing}")
        print(f"  rationale: {r.rationale}")
        print(f"  confidence  : {r.confidence}\n")
        