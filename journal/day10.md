# Coverage Matrix v2 — seed rows
Drafted: 2026-10-08 (Day 10, Card 1 check) · Rows 1-3 authored by Lily;
rows 4-5 drafted with Claude, golds ratified by Lily 2026-10-08.
Status: blueprint approved. Record texts: Sunday build. Lint runs before the
first expanded eval. Pre-registered prediction: the expanded exam breaks the
60/60 sweep; if it does not, the matrix was not aimed at boundaries.

Row 1 [EX-002 disambiguated sibling - HBC side]
Intent: Separate the clean side of the HBC/MRA boundary: bill amount surges
        while the meter story is verifiably clean (actual reads, increment
        consistent with usage, usage flat vs. 12-mo avg, no rate change) -
        bill computation is the only explanation left. Passes only if the
        bill-computation tiebreaker does its job; an MRA verdict = tiebreaker
        failed.
Gold:   High Bill Complaint / P2 / Billing Analyst
Note:   New record; EX-002 itself stays unchanged as the wobbler specimen.
        Pairs with Row 5.

Row 2 [probe: unconfirmed-discrepancy rule]
Intent: Test sentence 1 where it alone carries the verdict: member reports a
        money discrepancy that is explicitly UNVERIFIED (claim only, nothing
        confirmed in the system), with no service risk and no disconnection
        notice so the precedence clause stays silent. Placed in a different
        category from EX-019 (its origin) to test the rule generalizes.
        Passes only if P2; a P3 verdict = "unconfirmed" read as "can wait."
Gold:   High Bill Complaint / P2 / Billing Analyst
Note:   P3 twin (explanation-only request, no claimed error) = candidate row.

Row 3 [probe: precedence clause]
Intent: Stage the collision on purpose: an explicitly UNVERIFIED member-reported
        money discrepancy (fires the discrepancy rule -> P2) WHILE a
        disconnection notice is already in hand with a dated cutoff (fires
        precedence -> P1). Both sentences fire; precedence must win. Permanent
        regression test for the Sep 19 incident. Passes only if P1 both runs;
        a P2 verdict = the discrepancy rule downgraded imminent service risk.
Gold:   High Bill Complaint / P1 / Billing Analyst
Note:   Trigger used: notice-in-hand (dated). "Member without service" variant =
        candidate twin. Routing stays Billing Analyst per the Day-8 rule.

Row 4 [flavor-two contradiction: member claim vs. system data]
Intent: First coverage of the claim-vs-data contradiction flavor: member insists
        the home was VACANT all period, but AMI shows steady ACTUAL daily usage
        consistent with occupancy; no rate change, bill unremarkable. The
        conflict cannot be resolved at a desk - the identifiable next action is
        physical verification of the meter/premise association. Discriminates
        three ways: must land MRA + FSO, not HBC (desk review cannot answer a
        physical question) and not Other (a resolution path IS identifiable).
        Unverified money discrepancy -> P2 via sentence 1, generalized to a
        third category. Passes only if MRA / P2 / FSO.
Gold:   Meter Read Anomaly / P2 / Field Service Order
Note:   Gold ratified by shop ruling 10/08 (meter-verify outranks BA).

Row 5 [EX-002 disambiguated sibling - MRA side]
Intent: The other half of the Row 1 pair: bill surges AND the meter story is
        the suspect - reads jump far beyond the usage history (or the read
        sequence is impossible), rate unchanged. The meter data is the only
        abnormal element, so the verdict must be a truck roll, not a desk
        review. Passes only if MRA / Field Service Order; an HBC verdict = the
        tiebreaker over-rotated toward computation. Completes the
        both-directions test of the tiebreaker with Row 1.
Gold:   Meter Read Anomaly / P2 / Field Service Order

## Candidate rows 6+ (backlog, from known gaps + discoveries during drafting)
- Other "conflict prevents identifying the cause" branch: ZERO probes today -
  a total-conflict record with no identifiable path -> gold Other. (Found 10/08.)
- P3 twin of Row 2: explanation-only request, no claimed error -> P3.
- Precedence "member without service" twin of Row 3.
- Low-confidence targets; P1 variety beyond outages; more flavor-two coverage.
- Lint rule #3 (from Row 1's typo): flag any gold category outside the 6-value enum.