"""Shared triage fixtures: the exception texts the triage scripts run on.

Each record carries a stable id, the exception text, and a `gold` block holding
the human-labeled expected triage result (filled in by hand).
"""

EXCEPTIONS = [
    {
        "id": "EX-001",
        "text": """Acct 4471: Residential, rate R-1. Bill = $612 vs. 12-mo avg $185. Meter read actual (not estimated). Usage 4,890 kWh vs. avg 1,450. 
    Note: member called 3/12 claiming "nothing changed." No rate change on account. Prior month also elevated (2,900 kWh).""",
        "gold": {
            "category": "Meter Read Anomaly",
            "priority": "P2",
            "routing": "Field Service Order",
            "note": "the billing issue was due to surged kwh meter usage, will need a technical support to check the meter reading at the field",
        },
    },
    {
        "id": "EX-002",
        "text": """Acct 12345: residential, rate R-1. bill=$1000 vs last bill $100, meter read is 100, last month read was 80, 
    kwh usage is same for last and this month. member called claimed nothing has been changed.no rate change on the account""",
        "gold": {
            "category": "High Bill Complaint",
            "priority": "P2",
            "routing": "Billing Analyst",
            "note": "The high billing issue will need a billing analyst to research the root cause, since meter usage has been consistent, and there is no rate change.",
        },
    },
    {
        "id": "EX-003",
        "text": """Acct 11111: commercial, rate C-1, Bill = $10000 vs last bill $5000, meter read is estimated, 
    usage is doubled comparing to previous month.""",
        "gold": {
            "category": "Estimated Read Streak",
            "priority": "P2",
            "routing": "Billing Analyst",
            "note": "The usage for th bill has been doubled due to the estimated meter reading, since there is no actual reading, will need a billing analyst to check the estimation calculation",
        },
    },
        {
        "id": "EX-005",
        "text": """Acct 11111: member reports the rate code on the latest bill received is different from last month, and the member didn't know about the change.""",
        "gold": {"category": "Rate Code Mismatch", "priority": "P2", "routing": "Billing Analyst", "note": ""},
    },
    {
        "id": "EX-006",
        "text": """Acct 22222: net metering account, from the last bill, there is no recorded generation KWH and generation credits. Member is afraid the net meter may not working.""",
        "gold": {"category": "Net Metering True-Up", "priority": "P2", "routing": "Field Service Order", "note": ""},
    },
    {
        "id": "EX-007",
        "text": """Acct 33333: member has a big outstanding balance, wanted to set up an arrangement to pay over 3 months.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P3", "routing": "CSR Callback", "note": ""},
    },
    {
        "id": "EX-008",
        "text": """Acct 44444: member just had a thunderstorm last night, today there is no electricity, asking if utility is on it already and when the service is going to be restored.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P1", "routing": "CSR Callback", "note": ""},
    },
    {
        "id": "EX-009",
        "text": """Acct 55555: the customer service regarding billing related questions are getting slower these days, can we improve the response time.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P3", "routing": "CSR Callback", "note": ""},
    },
    {
        "id": "EX-010",
        "text": """Acct 66666: recently we had a meter change, then received a bill for this month, found the charge is $500, this based on the bill was due to reading surge after the meter change.""",
        "gold": {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", "note": ""},
    },
]

# Not a billing exception at all (an outage report). triage_v1 runs this one in
# addition to EXCEPTIONS to exercise its "Other / Needs Human Review" category;
# triage_v0 has no such category and never included it.
NON_BILLING_EXCEPTIONS = [
    {
        "id": "EX-004",
        "text": """Acct 7203: Member reports a vehicle struck the pole near their driveway last night; transformer damaged, power out at the residence. 
    No billing fields affected. Member asking when service will be restored.""",
        "gold": {
            "category": "Other / Needs Human Review",
            "priority": "P1",
            "routing": "CSR Callback",
            "note": "since the customer is having the electric outage, will need a CSR to review if any technical resources are currently working on the issue, and get the ETA to call the member",
        },
    },
]

CATEGORIES = {"High Bill Complaint", "Estimated Read Streak", "Rate Code Mismatch",
              "Net Metering True-Up", "Meter Read Anomaly", "Other / Needs Human Review"}
PRIORITIES = {"P1", "P2", "P3"}
ROUTINGS = {"CSR Callback", "Billing Analyst", "Field Service Order"}

if __name__ == "__main__":
    ids = [r["id"] for r in EXCEPTIONS]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for r in EXCEPTIONS:
        g = r["gold"]
        assert g["category"] in CATEGORIES, (r["id"], g["category"])
        assert g["priority"] in PRIORITIES, (r["id"], g["priority"])
        assert g["routing"] in ROUTINGS, (r["id"], g["routing"])
        assert "TODO" not in g["note"] and "<" not in r["text"], (r["id"], "unfinished")
    print(f"{len(EXCEPTIONS)} records OK")
