n=5 by eyeball
===== Exception 1 =====
  category : Meter Read Anomaly
  priority : P2
  routing  : Field Service Order
  rationale: The actual meter read yields 4,890 kWh versus a 12-month average of 1,450 kWh, with the prior month also elevated at 2,900 kWh, indicating a persistent read anomaly that cannot be explained by a rate change or member behavior, requiring field verification of the meter.
  confidence  : high

===== Exception 2 =====
  category : Other / Needs Human Review
  priority : P2
  routing  : Billing Analyst
  rationale: The bill increased 10x from $100 to $1000 while the meter reads (80->100) and kWh usage are reported as unchanged with no rate change on the account, creating a direct contradiction between the billed amount and the usage/rate data that cannot be resolved without human review.
  confidence  : low

===== Exception 3 =====
  category : Estimated Read Streak
  priority : P2
  routing  : Billing Analyst
  rationale: The current month's estimated read resulted in doubled kWh usage and a bill of $10,000 compared to last month's $5,000, representing a 100% increase with no rate change noted.
  confidence  : high

===== Exception 4 =====
  category : Other / Needs Human Review
  priority : P1
  routing  : CSR Callback
  rationale: Member reports active outage due to vehicle striking a pole and damaging the transformer, with no billing fields affected, making this a field emergency requiring immediate service restoration rather than a billing matter.
  confidence  : high


Did Acct 12345 flip to your gold label — and did its confidence drop if anything stayed ambiguous?
-the category is marked as other/needs human review, but actually i expected high bill complaint, but with this new run, the confidence level is droped to low. 

Did the rationales start citing your definitions ("read sequence is consistent, so not a meter anomaly") instead of vibes? 
not really. 



block 3 step 1: Design coverage before writing
                "High Bill Complaint",
                "Estimated Read Streak",
                "Rate Code Mismatch",
                "Net Metering True-Up",
                "Meter Read Anomaly",
                "Other / Needs Human Review"

each category has 1 clear case. total is 5. 
2 out of scope cases
one deliberate boundary case 
priority: p1, p2

    Meter Read Anomaly - """Acct 4471: Residential, rate R-1. Bill = $612 vs. 12-mo avg $185. Meter read actual (not estimated). Usage 4,890 kWh vs. avg 1,450. 
    Note: member called 3/12 claiming "nothing changed." No rate change on account. Prior month also elevated (2,900 kWh).""",
    High Bill Complaint -  """Acct 12345: residential, rate R-1. bill=$1000 vs last bill $100, meter read is 100, last month read was 80, 
    kwh usage is same for last and this month. member called claimed nothing has been changed.no rate change on the account""",
    Estimated Read Streak - """Acct 11111: commercial, rate C-1, Bill = $10000 vs last bill $5000, meter read is estimated, 
    usage is doubled comparing to previous month.""",

    Other / Needs Human Review - """Acct 7203: Member reports a vehicle struck the pole near their driveway last night; transformer damaged, power out at the residence. 
    No billing fields affected. Member asking when service will be restored.""",

    Rate Code Mismatch, P2, Billing Analyst, Acct 11111: member reports the rate code on the latest bill received is 
    different from last month, and the member didn't know about the change. 

    Net Metering True-Up, P2, Field Service Order, Acct 22222: net metering account, from the last bill, there is no recorded generation KWH and generation credits. 
    Member is afraid the net meter may not working.

    Other / Needs Human Review, P3, CSR Callback, Acct 33333: member has a big outstanding balance, wanted to set up an arrangement to pay over 3 months. 

    Other / Needs Human Review, P1, CSR Callback, Acct 44444: member just had a thunderstorm last night, today there is no electricity, asking if utility is on it already and
    when the service is going to be restored. 

    Other / Needs Human Review, P3, CSR Callback, Acct 55555: the customer service regarding billing related questions are getting slower these days, 
    can we improve the response time.

    Meter Read Anomaly, P2, Field Service Order, Acct 66666: recently we had a meter change, then received a bill for this month, found the charge is $500, 
    this based on the bill was due to reading surge after the meter change.   

