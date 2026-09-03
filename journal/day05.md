
## Week 1 Baseline
Date: 2026-09-02 · Commit:f4e16e7903b8aea18f07406364edcc03cbb86dd7 · Model: claude-sonnet-4-6 · n=20
Baseline file: results/run_20260902-2126.json · Replicate: results/run_20260902-2209.json

### 1. Overall accuracy (n=20)
| Field    | Accuracy | Correct/Total |
|----------|---------:|--------------:|
| Category |      95% |         19/20 |
| Priority |      85% |         17/20 |
| Routing  |      85% |         17/20 |
Table 1 — Overall accuracy. "Supports: the pipeline works end-to-end and lands far above the ~17% a random six-way guess would score, and no field is catastrophically broken. Cannot support: any precise accuracy claim, any 'good enough to ship' judgment."

### 2. Accuracy by gold category (category field)
| Gold category              | n | Correct | Accuracy | Misclassified as (id: predicted)   |
|----------------------------|--:|--------:|---------:|------------------------------------|
| High Bill Complaint        | 3 |       2 |      66% | —                                  |
| Meter Read Anomaly         | 3 |       3 |     100% |                                    |
| Estimated Read Streak      | 4 |       4 |     100% |                                    |
| Rate Code Mismatch         | 3 |       3 |     100% | —                                  |
| Net Metering True-Up       | 3 |       3 |     100% |                                    |
| Other / Needs Human Review | 4 |       4 |     100% | —                                  |

### 3. Escalation safety
| Direction                                   | Count | Ids    | Tolerance |
|---------------------------------------------|------:|--------|-----------|
| Dangerous: gold Other → predicted billing   |     0 | —      | 0         |
| Cheap: gold billing → predicted Other       |     0 |        |           |

### 4. Confidence calibration (category field)
| Stated confidence | n  | Correct | Accuracy |
|-------------------|---:|--------:|---------:|
| high              | 10 |      10 |     100% |
| medium            |  8 |       7 |      87% |
| low               |  2 |       2 |     100% |

### 5. Run-to-run wobble (baseline vs. replicate, identical spec)
| Field    | Baseline | Replicate | Records that flipped |
|----------|---------:|----------:|---------------------:|
| Category |      95% |       95% |        0             |
| Priority |      85% |       90% |        1 EX-019      |
| Routing  |      85% |       85% |        0             |

cost for one run: $0.11

I built a golden dataset and an offline eval harness for a domain triage agent, verified the harness itself before trusting it, established a commit-pinned baseline with a measured noise floor, and ran error analysis that routed every failure to the artifact that had to change — the labels, the spec, or the model.

## Block 3 — Miss review (baseline results/run_20260902-2126.json)

### Verdict lines (one per miss)
| id | Field | Gold → Predicted | Rationale (5 words) | Verdict | Evidence |
|----|-------|------------------|---------------------|---------|----------|
| EX-002 | category, routing | High Bill Complaint → Meter Read Anomaly | "usage increment inconsistent" | spec weak | meter read 80vs100 caused confusion |
| EX-012 | priority | P3 → P2 | "on-site meter read needed" | Gold wrong | P2 rule is explicit: included meter reading issue|
| EX-014| routing|CSR Callback-> Billing Analyst| unexpectedly high bill | Gold Wrong  | |
| EX-015 | routing | Billing Analyst -> CSR Callback |active service risk requiring callback| Spec Weak|
| EX-017 | Priority | P3 -> P2 | current bill reflects old rate | Gold Wrong | 
| EX-019 | Priority | P3 -> P2 | credit possible miscalculation or misapplication | gold wrong|
{
      "id": "EX-002",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P2",
      "gold_routing": "Billing Analyst",
      "pred_category": "Meter Read Anomaly",
      "pred_priority": "P2",
      "pred_routing": "Field Service Order",
      "confidence": "medium",
      "rationale": "The current meter read of 100 vs last month read of 80 produces a usage increment inconsistent with the $1000 bill versus last month's $100 bill and same reported kWh usage, suggesting the reads or meter cannot be trusted and require field verification.",
      "category_match": false,
      "priority_match": true,
      "routing_match": false
    },

    {
      "id": "EX-012",
      "gold_category": "Estimated Read Streak",
      "gold_priority": "P3",
      "gold_routing": "Field Service Order",
      "pred_category": "Estimated Read Streak",
      "pred_priority": "P2",
      "pred_routing": "Field Service Order",
      "confidence": "high",
      "rationale": "Customer reported 3+ consecutive months of estimated reads due to a locked gate, which has now been resolved, requiring a technician to perform an actual meter read on-site.",
      "category_match": true,
      "priority_match": false,
      "routing_match": true
    },

        {
      "id": "EX-014",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P2",
      "gold_routing": "CSR Callback",
      "pred_category": "High Bill Complaint",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "low",
      "rationale": "Member reports an unexpectedly high bill this month with actual reads and no rate changes on file, indicating the meter reads are trusted but the billed dollar amount is in dispute.",
      "category_match": true,
      "priority_match": true,
      "routing_match": false
    },

       {
      "id": "EX-015",
      "gold_category": "High Bill Complaint",
      "gold_priority": "P1",
      "gold_routing": "Billing Analyst",
      "pred_category": "High Bill Complaint",
      "pred_priority": "P1",
      "pred_routing": "CSR Callback",
      "confidence": "medium",
      "rationale": "Member received a disconnection notice tied to a disputed high bill charge with no resolution communicated yet, indicating active service risk requiring immediate callback.",
      "category_match": true,
      "priority_match": true,
      "routing_match": false
    },

        {
      "id": "EX-017",
      "gold_category": "Rate Code Mismatch",
      "gold_priority": "P3",
      "gold_routing": "Billing Analyst",
      "pred_category": "Rate Code Mismatch",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "medium",
      "rationale": "Member enrolled in budget billing this month but the current bill still reflects the old rate, indicating the rate change request may not have been applied to the account.",
      "category_match": true,
      "priority_match": false,
      "routing_match": true
    },

        {
      "id": "EX-019",
      "gold_category": "Net Metering True-Up",
      "gold_priority": "P3",
      "gold_routing": "Billing Analyst",
      "pred_category": "Net Metering True-Up",
      "pred_priority": "P2",
      "pred_routing": "Billing Analyst",
      "confidence": "low",
      "rationale": "Member reports their kWh credit balance is lower than expected, indicating a possible miscalculation or misapplication of net metering credits that requires a billing records review.",
      "category_match": true,
      "priority_match": false,
      "routing_match": true
    },
### Verdict tally
- Gold wrong: 4 · Spec weak: 2 · Model wrong: 0 · Undecided: 0
- Reading: misses cluster in the spec — next hour belongs to the prompt, not the model.

### The ONE change (for Thursday)
- Change: change the priority in gold set for EX-019 From P3 to P2
- Prediction: fix the priority mismatch
- NOT changed tonight. 