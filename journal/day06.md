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