"""Day 1: first triage prompt - the seed of the flagship project."""
from dotenv import load_dotenv
import anthropic

from exceptions import EXCEPTIONS

load_dotenv()
client = anthropic.Anthropic()

PROMPT_TEMPLATE = """You are a billing-exception triage assistant for an electric cooperative.

Classify the exception below.

Category (choose exactly one): High Bill Complaint | Estimated Read Streak |
Rate Code Mismatch | Net Metering True-Up | Meter Read Anomaly
Priority (choose exactly one): P1 (member-impacting, urgent) | P2 | P3
Routing (choose exactly one): CSR Callback | Billing Analyst | Field Service Order

Respond in exactly this format:
Category: <category>
Priority: <priority>
Routing: <routing>
Rationale: <one sentence citing specific data from the exception>

Exception:
{exception}"""

if __name__ == "__main__":
    for i, exc in enumerate(EXCEPTIONS, 1):
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(exception=exc)}],
        )
        print(f"===== Exception {i} =====\n{resp.content[0].text}\n")
