## Day 6 — Stage 1 prediction (written BEFORE the gold v2 rerun)

Changing gold only (4 labels), spec untouched at commit f4e16e7.
Baseline v1: category 19/20 · priority 17/20 · routing 17/20.

Derivation, per fix (model predictions from run_20260902-2126.json):
- EX-012 gold priority P3→P2. Model predicted P2 → miss becomes a hit. +1 priority
- EX-017 gold priority P3→P2. Model predicted P2 → miss becomes a hit. +1 priority
- EX-019 gold priority P3→P2. Model predicted P2 → miss becomes a hit. +1 priority
  (caveat: EX-019 is the known-flaky record — it flipped priority between
  identical runs, so this +1 is the least certain line here)
- EX-014 gold routing CSR Callback→Billing Analyst. Model predicted Billing
  Analyst → miss becomes a hit. +1 routing

Predicted baseline v2:
- Category: 19/20 (unchanged — EX-002 still misses; nothing tonight touches it)
- Priority: 20/20 (17 + 3)
- Routing:  18/20 (17 + 1; EX-002 and EX-015 remain, by design)

Tolerance: ±1 record per field (measured noise floor). EX-019 is the named
candidate if priority lands at 19/20 instead.

Would falsify the prediction: any *category* movement; more than one
unexpected flip; a record outside {012, 014, 017, 019} changing on a field
tonight's fixes don't touch.

## Day 6 — Baseline v2 (gold v2)

Date: 2026-09-03 · Commit: ⟨6ac597edd29c2e6aa05ca60564bc9174649d467e⟩ (gold v2) · Model: claude-sonnet-4-6 · n=20
File: results/⟨run_20260903-1912.json⟩ · Cost: ~$0.11
Supersedes: baseline v1 (run_20260903-2013.json, gold v1) — v1 numbers are
not comparable to anything after tonight.

| Field    | Predicted | Actual | Verdict |
|----------|----------:|-------:|---------|
| Category |     19/20 | ⟨19/20⟩ | ⟨held⟩ |
| Priority |     20/20 | ⟨20/20⟩ | ⟨held⟩ |
| Routing  |     18/20 | ⟨18/20⟩ | ⟨held⟩ |

Prediction line: ⟨held on all three fields; no unexpected flips — the four
corrected records became hits, EX-002 and EX-015 miss as designed.⟩

Carry-forward misses (the complete list): EX-002 (category, routing) ·
EX-015 (routing).


## Day 6 — Experiment: bill-computation tiebreaker

Date: 2026-09-03 · Commit: ⟨6ac597edd29c2e6aa05ca60564bc9174649d467e⟩ (spec change alone) · Compared against: baseline v2 (⟨run_20260903-2023.json⟩)
File: results/⟨run_20260903-2023.json⟩ · Cost: ~$0.11
Change (one variable): one tiebreaker sentence added to <category_definitions> after High Bill Complaint.

Prediction (from Day 5, pre-registered): fixes EX-002 category and routing;
changes nothing else; must beat the 1-record noise floor.

| Check | Predicted | Actual | Verdict |
|-------|-----------|--------|---------|
| EX-002 category → High Bill Complaint | flip to hit | ⟨hit⟩ | ⟨held⟩ |
| EX-002 routing → Billing Analyst      | flip to hit | ⟨hit⟩ | ⟨held⟩ |
| EX-015 routing (must stay a miss — untouched by this change) | miss | ⟨miss⟩ | ⟨held⟩ |
| Regression check: all 17 previously-passing records | no change | ⟨no change⟩ | ⟨held⟩ |

Overall verdict: ⟨PREDICTION HELD — record-specific claim confirmed, zero
regressions. Category 20/20, priority 20/20, routing 19/20.⟩

Interpretation: ⟨one sentence — e.g., "the definition layer, not the model,
was the missing piece for flavor-one contradictions — consistent with the
Day 5 verdict distribution."⟩