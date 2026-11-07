# Day 12 - Fix Week
2026-11-04 evening (cards 1-2) + 2026-11-07 (cards 3-4)

Baseline: v4, frozen (runs 2026-10-30 14:22 + 14:26: 29/30 category, 30/30
priority, 29/30 routing; EX-030 the only miss, RCM/BA both runs). Both
experiments below compare against v4. Spec state at end of day: v4, untouched -
both changes reverted per protocol.

## Scoreboard - the four runs (2026-11-04)

| Run   | Config                  | Cat   | Pri   | Route | EX-030          | Margin notes                          |
|-------|-------------------------|-------|-------|-------|-----------------|---------------------------------------|
| 22:30 | B: rationale field first| 29/30 | 30/30 | 29/30 | RCM / BA (med)  | n_high 17, med 12, low 1              |
| 22:32 | B: rationale field first| 29/30 | 30/30 | 29/30 | RCM / BA (med)  | n_high 15, med 12, low 3              |
| 22:44 | conflict clause in spec | 29/30 | 30/30 | 28/30 | Other / BA (med)| EX-002 -> MRA/FSO (med)               |
| 22:45 | conflict clause in spec | 29/30 | 30/30 | 29/30 | Other / BA (med)| EX-002 -> Other/BA (low) = over-esc   |

## Experiment B - rationale-first field order (card 1)

Change under test: move `rationale` to the FIRST property in the structured-output
schema used by triage(); nothing else. Pre-registered 2026-10-14; prediction:
accuracy same or better vs v4, all 29 stable records keep their verdicts, wobble
no higher than baseline (0 verdict flips), EX-030 expected unchanged. Falsifier:
any stable record moves, accuracy drops, or new wobble appears.

Result (2026-11-04, runs 22:30 + 22:32, rationale field first):
HELD on all clauses; falsifier silent. The reorder bought zero points.
- Accuracy identical to v4 in both runs (29/30 cat, 30/30 pri, 29/30 route);
  all 29 stable records kept their verdicts; 0 verdict flips between runs.
- EX-030 still RCM/BA (medium) both runs -> wrong 8/8 overall. Run-2 rationale
  NAMES the conflict ("adds unresolved complexity that lowers confidence") and
  still picks a lane: the missing piece is the rule, not the reasoning order.
- PM side-finding: reasoning-first hedges more (n_high ~18-19 -> 15-17, medium -> 12)
  at equal accuracy => under a high-only auto-file gate, automation rate falls
  with no accuracy gain.
- Label jitter unchanged (~2/pair: EX-006, EX-022) - consistent with the T=0 finding.
- DECISION: keep the current verdict-first field order.

Revert: git checkout, grep confirmed `rationale` back to last position before the
next experiment ran. Independent confirmation: the 22:44/22:45 runs' confidence
distribution snapped back to v4 shape (18 high vs B's 15-17).

## Conflict clause - first keeper change, first live-fire falsification (card 2)

Change under test, added to the Other / Needs Human Review definition in the spec
prompt (triage_v1.py), nothing else:

> If the evidence in a record supports more than one exception category and the
> record alone cannot establish which one is primary - the competing explanations
> are unverified - classify it as Other / Needs Human Review: a human must
> determine the primary issue before the record can be routed to a single queue.

Pre-registered prediction: EX-030 -> Other / CSR Callback in both runs; all 29
stable records keep their verdicts; over-escalation stays 0. Falsifier: EX-030
still lands RCM, OR any stable record moves, OR anything newly over-escalates to
Other (the clause caught healthy records = too broad).

Result (2026-11-04, runs 22:44 + 22:45, conflict clause added to Other definition):
FALSIFIED - falsifier clauses 2 and 3 fired. Clause reverted; spec back to v4; no commit.
- The target moved as designed: EX-030 -> Other / P2 in BOTH runs (first time in 10
  runs), rationale naming both unverified stories. But routing stayed Billing Analyst,
  not CSR Callback - even the win was partial. Follow-up: does the spec explicitly
  tie Other -> CSR Callback?
- EX-002 (stable-correct in all 8 prior runs) broke both runs, two different ways:
  MRA/FSO (medium) run 1, Other/BA (low) run 2 - the first verdict-level run-to-run
  flip of the n=30 era, and run 2 is the over-escalation the falsifier named. The
  clause read one unexplained symptom (10x bill, flat usage) as "competing
  explanations."
- Twin contrast is the diagnosis: EX-021 (same scenario, hatches closed) stayed
  HBC/high both runs; EX-022/EX-014 (soft but single-story) untouched. Blast radius
  = exactly the one record with a live second story.
- Scoreboard: category flat 29/30 (bought EX-030, paid EX-002); priority 30/30;
  routing DOWN (28/30, 29/30 vs v4's 29/30). The headline metric was flat - the
  stable-records falsifier clause, not accuracy, caught the damage.
- Calibration held through the failure: miss in medium then low, never high.
  Confidence distribution back to v4 shape (18 high) = independent proof the
  Experiment B revert landed. Single variable confirmed.
- NEXT (own pre-reg, not tonight): narrow the clause - require AFFIRMATIVE evidence
  for each competing category (EX-030 has two positive signals: unrequested rate
  code + 40% actual-read jump; EX-002 has one symptom with hypothesized causes).
  Separate thread: the Other -> CSR routing gap.

Revert verified 2026-11-04 23:02: grep for the clause -> nothing; grep known-positive
"Needs Human Review" -> 4 hits (lines 24/47/98/121); triage_v1.py clean in git status.
Note: this reverted sentence now exists ONLY in this journal - git never saw it.

## RAG card 1 - Retrieval (card 3, 2026-11-07)

Check: EX-030 carries two unverified stories (unrequested rate-code change vs a
real 40% jump in actual reads). Name the ONE document retrieval should fetch to
settle it - shelf, document, which story it kills, kill logic in both branches.

My answer: member history shelf, keyed by account 1530; first pass proposed two
fetches (rate-change request log + October read-source record). Graded PASS, with
three sharpenings:
- Ranking rule: a fetch earns its tokens only if its contents can FLIP the
  verdict. The rate-change log flips in every branch -> fetch #1. The read-source
  record half-passes: EX-030 already stamps the reads ACTUAL, so the confirming
  branch moves nothing. It is EX-024 insurance - fetch #2, not co-fetch #1.
- Kill-direction wiring (falsifier discipline again): member REQUESTED the change
  -> the rate-change story DIES (legitimate, member forgot; explanation case).
  Utility-initiated with a documented reason -> also dies as an exception.
  NO RECORD AT ALL -> smoking gun, unauthorized change confirmed. Absence is the
  finding: the settling document can settle by what it does NOT contain.
- Walked past: "which is the main reason" is an ARITHMETIC question and the
  arithmetic lives on shelf 2. Fetch the tariff sheets for both rate codes and
  recompute old rate x October kWh: lands near the doubled bill -> usage is the
  dollar driver; far below -> the rate code is. Legitimacy, instrument-trust,
  and primacy are three different retrieval jobs.
- Week 3 hook: EX-030 becomes the retriever's first test query. Third life:
  honesty probe -> clause falsifier -> retrieval test.

## Wrap (card 4)

DECISION register (standing):
- D1 (Day 11, Exp A): keep default sampling. T=0 connects the dial but buys no
  accuracy, and label jitter survives T=0 (greedy ties).
- D2 (Day 12, Exp B): keep verdict-first field order.
- D3 (Day 12, conflict clause): FALSIFIED -> reverted; spec stays v4. Clause v2
  (affirmative-evidence narrowing) queued behind the routing question.
- Baseline stays v4. Next keeper change that HOLDS -> next full exam = baseline v5.

Commits (made ✍️ 2026-11-__):
1. exp B: rationale-first field order HELD null - zero accuracy gain, more
   hedging; keep verdict-first
   (journal/day12.md, results/run_20261104-2230.json, -2232.json)  hash: ✍️
2. exp: conflict clause FALSIFIED - EX-030 escalates but EX-002 destabilized;
   spec reverted, baseline stays v4
   (results/run_20261104-2244.json, -2245.json)  hash: ✍️
Housekeeping: .DS_Store untracked + added to .gitignore  ✍️ done / skipped

Queue -> evenings (✍️ adjust days as needed):
- Mon 11-09: routing question - does the spec explicitly tie Other -> CSR
  Callback? Read the spec prompt, write a note, change nothing. (~15-20 min)
- Tue 11-10: lint rule 2 word list (add "cutoff" + any other gaps), then
  adjudicate the standing EX-004 / EX-008 advisories. (~30 min)
- Wed 11-11: response.usage wiring - measured token counts per run instead of
  hand estimates. (~20-30 min)
- Thu 11-12: EX-002 decision note - keep the open hatch deliberately (it is now
  a diagnostic twin) or pin the reads; either way write it down. Gold does not
  change without its own pre-reg. (~15 min)
- Parked: low-confidence target records; conflict clause v2 pre-reg (waits for
  the Mon routing note).

Hours: cards 1+2 ✍️ (Wed evening) · cards 3+4 ✍️ (Sat) · Day 12 total ✍️