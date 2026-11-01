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
    {   "id": "EX-021",
            "text": """Acct 1021: residential, rate R-1. bill=$1000 vs last bill $100, kwh usage is same for last and this month, 
            both reads are actual (not estimated). Member called claimed nothing has been changed. no rate change on the account """,
            "gold": {"category": "High Bill Complaint", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "no usage difference between last month and this month, also no rate change, requires bill calculation verification."},
            }, 
    {   "id": "EX-022",
            "text": """Acct 1022: member called, says this month's bill doesn't match her own
                records - she tracked her payments and believes the amount is wrong, but
                can't point to which charge. nothing changed on the account per member.
                requests verification.""",
            "gold": {"category": "High Bill Complaint", "priority": "P2", "routing": "Billing Analyst", 
                    "note": "unverified member-claimed money discrepancy, no specific charge identified, no service risk -> P2 by the unverified-discrepancy rule,"
                    " even unconfirmed.Passes only if NOT downgraded to P3 as a routine billing question."},
            }, 
    {   "id": "EX-023",
            "text": """Acct 1023: member called, says this month's bill is much higher than last
                month but can't say where it went wrong - wants it checked before she pays.
                The disputed balance is unpaid, and the account is now on the cutoff list:
                disconnection scheduled for tomorrow.""",
            "gold": {"category": "High Bill Complaint", "priority": "P1", "routing": "Billing Analyst", 
                    "note": """unverified bill dispute + disconnection notice in hand (dated: tomorrow).
                        Precedence clause -> P1: service risk outranks, and the unverified-discrepancy
                        rule does NOT hold it at P2. Tiebreaker 2 -> routing stays Billing Analyst:
                        correcting the bill is what removes the service risk.
                        Passes only if P1 in both runs AND routing = BA. Regression test for the
                        Sep 19 precedence experiment."""},
            }, 
    {   "id": "EX-024",
            "text": """Acct 1024: member called and says she was in China for last three months, the home was VACANT all period, 
            but AMI shows steady ACTUAL daily usage consistent with occupancy; no rate change.""",
            "gold": {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", 
                    "note": "vacant home points to no usage should be reported that is conflict with AMI daily usage report, this meter reading issue "
                    "will need a field service order to verify the meter reading"},
            }, 
    {   "id": "EX-025",
            "text": """Acct 1025: member called, says the bill surged this month. Average usage
                is ~200 kwh/month; this month shows 20,000 kwh, and BOTH months' reads are
                ACTUAL meter reads. Member says it's impossible - even with every appliance
                and light running all day, a one-bedroom apartment could not use that much
                in a month. No rate change, and no recent meter work on the account. """,
            "gold": {"category": "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order", 
                    "note": """reads genuinely jumped (200 -> 20,000, 100x; physically impossible for a
                        1-BR: even 10 kW nonstop x 720h = 7,200 kwh) -> the reads themselves are
                        the suspect part -> MRA / P2 / FSO. Sibling of EX-021: same surface,
                        opposite pivotal evidence. Passes only if MRA (not HBC) AND FSO (not BA);
                        if EX-021 and EX-025 land on the same side, the tiebreaker failed."""},
            }, 
{   "id": "EX-026",
            "text": """Acct 1026: member called, says she just received the October bill and
                noticed the same $45 billing adjustment appears twice on it. Asking if
                someone can check whether it was billed incorrectly. """,
            "gold": {"category":  "High Bill Complaint", "priority": "P2", "routing": "Billing Analyst",
                    "note": """rclean-evidence HBC: visible duplicate adjustment on the bill = concrete
                        computation evidence -> analyst verification. Calibration anchor: this
                        record SHOULD come back high confidence."""},
            },   
{   "id": "EX-027",
            "text": """Acct 1027: member called, says she was on an overseas trip and missed the
                payment deadline for the outstanding balance. A disconnection notice has been
                issued - cutoff scheduled tomorrow. Nothing about the bill is disputed; she
                wants to know how to avoid the cutoff if she pays today. """,
            "gold": {"category":  "Other / Needs Human Review", "priority": "P1", "routing": "CSR Callback",
                    "note": """RULING: no billing exception exists - the bill is correct and
                        uncontested, so NOT High Bill Complaint despite the bill/cutoff vocabulary
                        (that bait is the test). None of the five specific categories fit a pure
                        payment-logistics matter -> Other / Needs Human Review. P1 anchored to the
                        precedence clause: a disconnection notice has been issued, and the clause
                        does not require a dispute. Routing CSR Callback: nothing for an analyst to
                        verify, nothing for the field; member needs human contact today (pay by
                        today -> account comes off the cutoff list).
                        Passes only if: Other (not HBC), P1 (not P3 routine inquiry), CSR Callback. """},
            },   
{   "id": "EX-028",
            "text": """Acct 1028: member called, says she just received the October bill and got a high bill. 
            The house had a meter change during the middle of the month, customer found the the usage with the 
            old meter and new meter together is more than 1000 kwh, but the average kwh for this whole year is 
            only 50 kwh per month. """,
            "gold": {"category":  "Meter Read Anomaly", "priority": "P2", "routing": "Field Service Order",
                    "note": """"RULING: FSO over desk re-bill. Competing theory (rejected): exchange reads
                        is-entered -> Billing Analyst desk review + re-bill. FSO wins per tiebreaker 1
                        (the meter must be verified before the bill can be trusted) and because the old
                        meter's final read can only be confirmed against the physical device before it
                        is wiped/recycled - field verification is time-sensitive, re-billing is not.
                        P2: member-reported money discrepancy, no service risk.
                        Passes only if MRA (not HBC) and FSO (not BA). Clean evidence - expect high
                        confidence."""},
            }, 
{
       "id": "EX-029",
            "text": """Acct 1029: member called, says she is getting bill due date alert every hour, but used to
             only get the alert once per month. """,
            "gold": {"category":  "Other / Needs Human Review", "priority": "P3", "routing": "CSR Callback",
                    "note": """multiple times of due date alert in one day is abnormal, CSR will need to verify 
                    the situation and report to IT department to fix the issue, due to no money related and no 
                    service is at risk, so it's P3."""},            
},
{
       "id": "EX-030",
              "text": """Acct 1030: member called, says her October bill roughly doubled. The bill
         shows a new rate code effective this cycle - she never requested a rate
         change. Her actual usage also jumped about 40% vs September (both months
         actual reads). Nothing verified yet on either side.""",
              "gold": {"category": "Other / Needs Human Review", "priority": "P2", "routing": "CSR Callback",
        "note": """Conflicted-Other probe: TWO independent, unverified explanations -
        unrequested rate-code change (Rate Code Mismatch story) AND a same-cycle
        actual-reads jump (Meter Read Anomaly story). Neither alone cleanly produces
        a doubled bill; choosing either category means ignoring live evidence ->
        escalate per the escape hatch. P2: member-reported money discrepancy,
        unverified, no service risk.
        Passes only if: category = Other (not RCM, not MRA) AND stated confidence
        at most medium. This is the honesty-clause probe."""},
}
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
