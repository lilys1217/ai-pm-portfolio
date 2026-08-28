"""Day 2: structured triage - schema-guaranteed JSON + client-side validation."""
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel
import anthropic

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

EXCEPTIONS = [
    """Acct 4471: Residential, rate R-1. Bill = $612 vs. 12-mo avg $185. Meter read actual (not estimated). Usage 4,890 kWh vs. avg 1,450. 
    Note: member called 3/12 claiming "nothing changed." No rate change on account. Prior month also elevated (2,900 kWh).""",
    """Acct 12345: residential, rate R-1. bill=$1000 vs last bill $100, meter read is 100, last month read was 80, 
    kwh usage is same for last and this month. member called claimed nothing has been changed.no rate change on the account""",
    """Acct 11111: commercial, rate C-1, Bill = $10000 vs last bill $5000, meter read is estimated, 
    usage is doubled comparing to previous month.""",
    """Acct 7203: Member reports a vehicle struck the pole near their driveway last night; transformer damaged, power out at the residence. 
    No billing fields affected. Member asking when service will be restored."""
]

def triage(exception_text: str) -> TriageResult:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=(
            "You are a billing-exception triage assistant for an electric "
            "cooperative. Base the rationale only on data present in the exception."
            "If the exception does not clearly fit a billing category, use 'Other / Needs Human Review'. Report confidence honestly."
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
    for i, exc in enumerate(EXCEPTIONS, 1):
        r = triage(exc)
        print(f"===== Exception {i} =====")
        print(f"  category : {r.category}")
        print(f"  priority : {r.priority}")
        print(f"  routing  : {r.routing}")
        print(f"  rationale: {r.rationale}")
        print(f"  confidence  : {r.confidence}\n")
        