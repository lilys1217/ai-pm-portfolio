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
    for i, exc in enumerate(EXCEPTIONS + NON_BILLING_EXCEPTIONS, 1):
        r = triage(exc)
        print(f"===== Exception {i} =====")
        print(f"  category : {r.category}")
        print(f"  priority : {r.priority}")
        print(f"  routing  : {r.routing}")
        print(f"  rationale: {r.rationale}")
        print(f"  confidence  : {r.confidence}\n")
        