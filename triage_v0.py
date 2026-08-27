"""Day 1: first triage prompt - the seed of the flagship project."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

EXCEPTIONS = [
    """Acct 4471: Residential, rate R-1. Bill = $612 vs. 12-mo avg $185. Meter read actual (not estimated). Usage 4,890 kWh vs. avg 1,450. 
    Note: member called 3/12 claiming "nothing changed." No rate change on account. Prior month also elevated (2,900 kWh).""",
    """Acct 12345: residential, rate R-1. bill=$1000 vs last bill $100, meter read is 100, last month read was 80, 
    kwh usage is same for last and this month. member called claimed nothing has been changed.no rate change on the account """,
    """Acct 11111: commercial, rate C-1, Bill = $10000 vs last bill $5000, meter read is estimated, 
    usage is doubled comparing to previous month.""",
]

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

for i, exc in enumerate(EXCEPTIONS, 1):
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(exception=exc)}],
    )
    print(f"===== Exception {i} =====\n{resp.content[0].text}\n")