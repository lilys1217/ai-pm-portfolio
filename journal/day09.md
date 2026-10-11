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
Status: EXECUTED 2026-09-19 — record below.

## Experiment: priority precedence clause (executed 2026-09-19)
Commit: ⟨hash⟩ (spec change alone) · Compared against: 2026-09-18 run pair
Runs: results/⟨run1⟩.json · results/⟨run2⟩.json · Cost: ~$0.22

| Check | Predicted | Run 1 | Run 2 | Verdict |
|---|---|---|---|---|
| EX-015 priority restored to P1 | P1 | P1 ✓ | P1 ✓ | HELD |
| EX-019 stays P2 (clause must not reach it) | P2 | P2 ✓ | P2 ✓ | HELD — no overreach |
| All other records unchanged | hold | clean | clean | HELD |

Overall verdict: PREDICTION HELD IN FULL — and the first clean sweep:
category 20/20 · priority 20/20 · routing 20/20, on BOTH runs. 120 checks
green across the pair. Noise floor on this pair: 0 records.

Notes:
- EX-019: discharge CONFIRMED — four consecutive stable P2 runs since the
  impact rule (2 on 09-18, 2 today). Root cause remains: under-specified
  boundary, fixed by policy sentence.
- EX-002: clean on both runs. STAYS on the watch list — one clean pair is
  within a wobbler's established behavior; logged as evidence, not
  acquittal.
- <priority_rules> now reads as a system: general impact rule → discrepancy
  clarification (09-18) → precedence clause (09-19). Each sentence traceable
  to the record that demanded it (EX-019, EX-015).

Instrument note (the honest half of a perfect score): the accuracy metric
has no headroom left — future experiments on this set can only reveal
regressions, never improvements — and the calibration table degenerates on
a clean sweep (every confidence bucket reads 100%, so the relationship it
audits has nothing to show). The set is outgrown. Sunday's expansion is now
necessary, not merely scheduled.

A perfect score doesn't mean the model is finished — it means the exam is.

## Build: lint rules
Commit: 36d0433 — lint_checks() added to classifier_v0.py, gold + predictions,
scoring untouched. Advisory only: prints after the report, flags for a human,
never auto-corrects, writes nothing.
Rule ① P3 + Field Service Order (a truck roll for a low-priority item).
Rule ② P1 whose text carries none of: outage / no power / without power /
disconnect.

First run output (replayed over results/run_20260919-1658.json — the clean
sweep; lint reads saved rows, so no new model calls):

    LINT [gold] EX-004: P1 without outage/disconnection language — verify by hand
    LINT [pred] EX-004: P1 without outage/disconnection language — verify by hand
    LINT [gold] EX-008: P1 without outage/disconnection language — verify by hand
    LINT [pred] EX-008: P1 without outage/disconnection language — verify by hand

### Hand-verify verdicts (2 records, 4 lines — on a clean sweep gold and pred agree)
| id | Fired | Text evidence | Verdict |
|----|-------|---------------|---------|
| EX-004 | ② | "transformer damaged, power out at the residence" | Lint wrong — gold P1 correct (member currently without service) |
| EX-008 | ② | "today there is no electricity … when the service is going to be restored" | Lint wrong — gold P1 correct (member currently without service) |

Tally: wrong golds caught 0 · model errors caught 0 · false positives 2.
Contrast with Day 5 (4 wrong golds, 0 model errors): that lint was pointed at a
set that still had wrong golds in it. This one is pointed at a set whose golds
have been ratified four runs deep — a clean sweep leaves lint nothing to find.
Day 5's asymmetry still holds, though: both firings are about gold, not the
model.

Root cause of both false positives: rule ②'s vocabulary is narrower than the
spec rule it is supposed to police. <priority_rules> makes P1 "currently
without service OR facing disconnection"; the vocabulary only recognizes how
the second half gets phrased. "power out" and "no electricity" are how the
first half actually reads, and neither is in the list.

Rule ① fired on nothing: no record in the 20 carries P3 + FSO on either side.
It is specified but unexercised — proven only against synthetic rows, not real
data. The expanded set will not exercise it either (day10 Rows 4/5 are P2 + FSO).

### The ONE change (candidate, NOT made tonight)
- Change: extend rule ②'s vocabulary with the without-service half of the P1
  rule — "power out", "no electricity", "service out", "lights out".
- Prediction: EX-004 and EX-008 go quiet and the 20-record set reads
  LINT: clean.
- Risk to watch: a quieter rule ② is a weaker rule ②. Lint earns its keep by
  firing on a P1 that should not be P1, and that event has not happened on this
  set yet. Widening the vocabulary before lint has ever caught a real miss
  tunes the instrument to the only data it has seen.

