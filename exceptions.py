"""Shared triage fixtures: the exception texts the triage scripts run on."""

EXCEPTIONS = [
    """Acct 4471: Residential, rate R-1. Bill = $612 vs. 12-mo avg $185. Meter read actual (not estimated). Usage 4,890 kWh vs. avg 1,450. 
    Note: member called 3/12 claiming "nothing changed." No rate change on account. Prior month also elevated (2,900 kWh).""",
    """Acct 12345: residential, rate R-1. bill=$1000 vs last bill $100, meter read is 100, last month read was 80, 
    kwh usage is same for last and this month. member called claimed nothing has been changed.no rate change on the account""",
    """Acct 11111: commercial, rate C-1, Bill = $10000 vs last bill $5000, meter read is estimated, 
    usage is doubled comparing to previous month.""",
]

# Not a billing exception at all (an outage report). triage_v1 runs this one in
# addition to EXCEPTIONS to exercise its "Other / Needs Human Review" category;
# triage_v0 has no such category and never included it.
NON_BILLING_EXCEPTIONS = [
    """Acct 7203: Member reports a vehicle struck the pole near their driveway last night; transformer damaged, power out at the residence. 
    No billing fields affected. Member asking when service will be restored.""",
]
