# Day 9 — 2026-09-18

## Shop ruling: unconfirmed money discrepancy = P2 (written before any run)
Ruling: every member-reported money discrepancy is treated as a money error
in flight until verified — P2, even when unconfirmed.
Why (policy, not model output): an unverified discrepancy does not wait. The
billing system keeps acting on the disputed balance — it carries forward,
ages toward delinquency, collection, and cutoff, and each stage adds
charges. The member is financially affected from the moment of report.
(Twelve years of CIS floors: discrepancies that wait become bigger, more
expensive problems.)

## Experiment: P2/P3 impact rule (spec sentence + gold note, one logical change)
Commit: ⟨hash⟩ · Change: <priority_rules> +2 sentences (rule + mechanism);
exceptions.py EX-019 note only (gold priority unchanged, P2)
Compared against: results/⟨current-baseline⟩.json
Runs: results/⟨run1⟩.json · results/⟨run2⟩.json · Cost: ~$0.22

Prediction (pre-registered): EX-019 = P2 on BOTH runs, matching gold; all
other records unchanged; ±1-record noise floor applies to each run
independently. Would falsify: EX-019 split across runs; EX-019 opposite the
ruling twice; any other record moving on priority.

| Check | Predicted | Run 1 | Run 2 | Verdict |
|---|---|---|---|---|
| EX-019 priority P2, matching gold | hold | P2 ✓ | P2 ✓ | HELD — discharged |
| Other records: priority unchanged | hold | EX-015 P1→P2 ✗ | EX-015 P1→P2 ✗ | FAILED — consistent = signal |
| Other records: category/routing | hold | EX-002 cat+routing flip | clean | 1 record, 1 run — noise floor |

Overall verdict: held on the target; failed the regression clause on EX-015.

Attribution:
- EX-015 (both runs → signal, attributed to tonight's change): the new
  sentence's consequence list ("delinquency, disconnection, and added
  charges") composed with the Day-8 routing sentence ("correcting the bill
  removes the service risk") to read a disconnection notice IN HAND as a
  future consequence inside a P2 pattern. Spec gap identified: no precedence
  between the discrepancy rule and the P1 rule. Gold stays P1 — correct
  under the impact axis: notice in hand = imminent risk = today's impact,
  not tomorrow's compounding.
- EX-002 (run 1 only → noise-floor citizen, new wobbler candidate): the
  contradiction probe argued the tiebreaker's hinge the other way ("delta
  inconsistent with member's claim" → reads don't cohere → meter
  implicated). Confidence was LOW on the miss — honesty clause and
  calibration working as designed on the record built to test them.

## Wobbler watch list
- EX-019: DISCHARGED 2026-09-18 — stable P2 across both runs after the
  impact rule. Five flips over two weeks, root cause: under-specified
  boundary, fixed by policy sentence.
- EX-002: admitted 2026-09-18 — 1 flip in 2 runs. Watch only; no action.

## Next experiment (pre-registered): priority precedence clause
Change (one sentence in <priority_rules>): imminent service risk outranks —
if the member is without service or a disconnection notice has been issued,
priority is P1; the discrepancy rule does not downgrade imminent risk.
Prediction: EX-015 = P1 on both runs; EX-019 STAYS P2 (its text carries no
service risk, so the clause must not reach it); nothing else moves.
Status: ⟨queued — Sunday's first 20 minutes | run tonight: result …⟩

## Build: lint rules
Commit: ⟨hash⟩ — lint_checks() added to classifier_v0.py, gold + predictions,
scoring untouched. First run output: ⟨"LINT: clean" | fired on EX-0xx: …⟩

first run: EX-002 and EX-015 got mismatches, EX-019 is good. 
{
      "id": "EX-002",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P2",
      "gold_routing": "Billing Analyst",
      "pred_category": "Meter Read Anomaly",
      "pred_priority": "P2",
      "pred_routing": "Field Service Order",
      "confidence": "low",
      "rationale": "The current read of 100 vs last read of 80 yields a delta inconsistent with 'same usage as last month' while the bill jumped from $100 to $1,000 with no rate change, indicating the billed kWh and dollar amount cannot both be trusted from these reads.",
      "category_match": false,
      "priority_match": true,
      "routing_match": false
    },

    {
      "id": "EX-015",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P1",
      "gold_routing": "Billing Analyst",
      "pred_category": "High Bill Complaint",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "medium",
      "rationale": "Member received a disconnection notice tied to an outstanding balance stemming from a disputed high bill with no resolution yet, requiring billing record investigation to correct the bill and remove the service risk before disconnection occurs.",
      "category_match": true,
      "priority_match": false,
      "routing_match": true
    },
    {
      "id": "EX-019",
      "gold_category": "Net Metering True-Up",
      "gold_priority": "P2",
      "gold_routing": "Billing Analyst",
      "pred_category": "Net Metering True-Up",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "low",
      "rationale": "Member reports banked kWh credit balance is lower than expected, indicating a possible misapplication or miscalculation of net metering credits requiring billing record review.",
      "category_match": true,
      "priority_match": true,
      "routing_match": true
    },

    for the second run: got false on priority_matc for EX-015 only, others are fine. 
        {
      "id": "EX-015",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P1",
      "gold_routing": "Billing Analyst",
      "pred_category": "High Bill Complaint",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "medium",
      "rationale": "Member received a disconnection notice tied to a disputed high bill surge that has not yet been reviewed or resolved, requiring billing records investigation to correct the bill and remove the service risk.",
      "category_match": true,
      "priority_match": false,
      "routing_match": true
    },
    {
      "id": "EX-019",
      "gold_category": "Net Metering True-Up",
      "gold_priority": "P2",
      "gold_routing": "Billing Analyst",
      "pred_category": "Net Metering True-Up",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "low",
      "rationale": "Member reported that their kWh credit balance is lower than expected, suggesting possible misapplication or miscalculation of banked credits that requires billing record review.",
      "category_match": true,
      "priority_match": true,
      "routing_match": true
    },
