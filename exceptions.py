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
            "note": "consecutive surged kwh meter usage for "
            "two months + unusual high bill amount",
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
            "note": "usage and rate unchanged while the bill jumped 10x → the bill computation itself is implicated",
        },
    },
    {
        "id": "EX-003",
        "text": """Acct 11111: commercial, rate C-1, meter read is the third consecutive estimated read, usage is doubled comparing to average usage.""",
        "gold": {
            "category": "Estimated Read Streak",
            "priority": "P2",
            "routing": "Billing Analyst",
            "note": "third consecutive estimated read — streak rule applies regardless of the doubled amount; "
            "expect a catch-up variance when an actual read arrives.",
        },
    },
    {
            "id": "EX-004",
            "text": """Acct 7203: Member reports a vehicle struck the pole near their driveway last night; transformer damaged, power out at the residence. 
        No billing fields affected. Member asking when service will be restored.""",
            "gold": {
                "category": "Other / Needs Human Review",
                "priority": "P1",
                "routing": "CSR Callback",
                "note": "damaged transformer + power out, out of scope, "
                "not billing+reading+meter related, need human review ",
            },
    },
    {
        "id": "EX-005",
        "text": """Acct 11115: member reports the rate code on the latest bill received is different from last month, and the member didn't know about the change.""",
        "gold": {"category": "Rate Code Mismatch", "priority": "P2", "routing": "Billing Analyst", 
                 "note": "different rate number shows on new bill"},
    },
    {
        "id": "EX-006",
        "text": """Acct 22222: net metering account, from the last bill, there is no recorded generation KWH and generation credits. Member is afraid the net meter may not working.""",
        "gold": {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", 
                 "note": "account shows net metering active, but no kwh generation"},
    },
    {
        "id": "EX-007",
        "text": """Acct 33333: member has a big outstanding balance, wanted to set up an arrangement to pay over 3 months.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P3", "routing": "CSR Callback", 
                 "note": "arrangement request, out of scope, need human review"},
    },
    {
        "id": "EX-008",
        "text": """Acct 44444: member just had a thunderstorm last night, today there is no electricity, asking if utility is on it already and when the service is going to be restored.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P1", "routing": "CSR Callback", 
                 "note": "called in to check outage status "},
    },
    {
        "id": "EX-009",
        "text": """Acct 55555: the customer service regarding billing related questions are getting slower these days, can we improve the response time.""",
        "gold": {"category": "Other / Needs Human Review", "priority": "P3", "routing": "CSR Callback", 
                 "note": "not physical billing or meter reading issues, out of scope, complaints only"},
    },
    {
        "id": "EX-010",
        "text": """Acct 66666: recently we had a meter change, then received a bill for this month, found the charge is $500, this was due to reading surge after the meter change.""",
        "gold": {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", 
                 "note": "surged meter reading caused high bill, need check readings for the old and new meters"},
    },
    {
        "id": "EX-011",
        "text": """Acct 11: recently I have got estimated reads for last 4 consecutive months. 
        The usage now is above average actual usage.""",
        "gold": {"category": "Estimated Read Streak", "priority": "P2", "routing": "Billing Analyst", 
                "note": "3+ consecutive estimated reads, bill drifting from actual usage"},
    },
    {   "id": "EX-012",
        "text": """Accet 12: customer called in mentioned he has been getting estimated reads and estimated bill for 
         more than 3 months, seems like it's due to the locked gate. now it's fixed, request actual read check """,
        "gold": {"category": "Estimated Read Streak", "priority": "P2", "routing": "Field Service Order", 
                "note": "Estimates caused by inaccessible meter (locked gate, dog) → access order"},
        },
    {   "id": "EX-013",
            "text": """Acct 13: my electric service has been getting four estimated read, then I got the bill
             this month is really high, want to know what's going on """,
            "gold": {"category": "Estimated Read Streak", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Catch-up bill after estimates; member complains about the high bill; cause over symptom"},
            },
    {   "id": "EX-014",
            "text": """Acct 14: got a really high bill this month, it's actual reading and no rate changes""",
            "gold": {"category": "High Bill Complaint", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Usage genuinely up, both reads actual, meter not implicated"},
            },
    {   "id": "EX-015",
            "text": """Acct 15: hi I just got the disconnection notice due to the outstanding unpaid balance, 
             but that balance was due to a recent surged high bill, I requested to dispute the bill but has not
               heard from the utlity yet. Can someone help me with this case? """,
            "gold": {"category": "High Bill Complaint", "priority": "P1", "routing": "Billing Analyst", 
                    "note": "Disconnection notice issued on a disputed bill → P1 by rule"},
            },
    {   "id": "EX-016",
            "text": """Acct 16: resident account with non demand meter, found my new bill is based on 
            commercial demand meter rate. please check.""",
            "gold": {"category": "Rate Code Mismatch", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Residential account billed on a commercial/demand rate"},
            },
    {   "id": "EX-017",
            "text": """Acct 17: resident account signed up for budget bill this month, but on the bill, it is still 
              the old rate. can someone check if my rate change request was actually done and saved under my account?  """,
            "gold": {"category": "Rate Code Mismatch", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Correct rate, wrong effective date (or seasonal rate not switched)"},
            },
    {   "id": "EX-018",
            "text": """Acct 18: I just received my settlement bill, but didn't see the kwh credits I 
            earned over last three months. """,
            "gold": {"category": "Net Metering True-Up", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Annual true-up: banked kWh credits missing from the settlement bill"},
            },
    {   "id": "EX-019",
            "text": """Acct 19: by checking my account for kwh credit balance, I found it's lower than my expectation. can 
             someone verify the calculation and explain to me? """,
            "gold": {"category": "Net Metering True-Up", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Credits present, member questions the calculation"},
            },
    {   "id": "EX-020",
            "text": """Acct 20: something strange going on, my kwh credit balance after last month's settlement - credit applied 
             to my outstanding balance should be reset to 0, but now I still have the credit balance from last year, you may want
              check your system and data, see if anything is going wrong. """,
            "gold": {"category": "Net Metering True-Up", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "Generation recorded and plausible, but the credit math is wrong — banked "
                    "credits applied at the wrong rate, or the balance not reset after the annual true-up. "
                    "Distinguishes billing-math errors from the register-fault rule (that's MRA)"},
            },        
]

# Not a billing exception at all (an outage report). triage_v1 runs this one in
# addition to EXCEPTIONS to exercise its "Other / Needs Human Review" category;
# triage_v0 has no such category and never included it.


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
