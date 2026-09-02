"""Day 3: score triage_v1 against the hand-labeled gold block in exceptions.py.

Runs every record through triage(), compares category / priority / routing to
`gold`, and reports overall accuracy, per-category accuracy, escalation safety
(the two directions of Other-vs-billing confusion), and a confidence
calibration table. Every row plus the summary is written to results/.
"""
import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

from exceptions import EXCEPTIONS
from triage_v1 import triage

HUMAN_REVIEW = "Other / Needs Human Review"
CONFIDENCE_ORDER = ["high", "medium", "low"]


def run(records):
    """Triage each record and return one comparison row per record."""
    rows = []
    total = len(records)
    for i, rec in enumerate(records, 1):
        gold = rec["gold"]
        result = triage(rec["text"])
        row = {
            "id": rec["id"],
            "gold_category": gold["category"],
            "gold_priority": gold["priority"],
            "gold_routing": gold["routing"],
            "pred_category": result.category,
            "pred_priority": result.priority,
            "pred_routing": result.routing,
            "confidence": result.confidence,
            "rationale": result.rationale,
            "category_match": result.category == gold["category"],
            "priority_match": result.priority == gold["priority"],
            "routing_match": result.routing == gold["routing"],
        }
        rows.append(row)
        marks = "".join(
            "OK " if row[k] else "XX "
            for k in ("category_match", "priority_match", "routing_match")
        )
        print(
            f"[{i}/{total}] {row['id']}  cat/pri/rou: {marks.strip()} "
            f"| {row['pred_category']} / {row['pred_priority']} / "
            f"{row['pred_routing']} ({row['confidence']})"
        )
    return rows


def summarize(rows):
    """Build the summary dict: overall, per-category, escalation, calibration."""
    n = len(rows)

    def acc(key):
        hits = sum(1 for r in rows if r[key])
        return {"correct": hits, "total": n, "accuracy": hits / n if n else 0.0}

    overall = {
        "category": acc("category_match"),
        "priority": acc("priority_match"),
        "routing": acc("routing_match"),
    }

    per_category = {}
    by_gold = defaultdict(list)
    for r in rows:
        by_gold[r["gold_category"]].append(r)
    for cat, group in sorted(by_gold.items()):
        hits = sum(1 for r in group if r["category_match"])
        per_category[cat] = {
            "correct": hits,
            "total": len(group),
            "accuracy": hits / len(group),
        }

    missed = [  # gold says human review, model claimed a billing category
        r for r in rows
        if r["gold_category"] == HUMAN_REVIEW and r["pred_category"] != HUMAN_REVIEW
    ]
    over = [  # gold is a billing category, model punted to human review
        r for r in rows
        if r["gold_category"] != HUMAN_REVIEW and r["pred_category"] == HUMAN_REVIEW
    ]
    escalation = {
        "missed_human_review": {
            "count": len(missed),
            "ids": [r["id"] for r in missed],
            "detail": [
                {"id": r["id"], "predicted": r["pred_category"]} for r in missed
            ],
        },
        "over_escalated_to_human_review": {
            "count": len(over),
            "ids": [r["id"] for r in over],
            "detail": [{"id": r["id"], "gold": r["gold_category"]} for r in over],
        },
    }

    counts = Counter(r["confidence"] for r in rows)
    calibration = {}
    levels = CONFIDENCE_ORDER + sorted(set(counts) - set(CONFIDENCE_ORDER))
    for level in levels:
        group = [r for r in rows if r["confidence"] == level]
        if not group:
            continue
        hits = sum(1 for r in group if r["category_match"])
        calibration[level] = {
            "count": len(group),
            "correct": hits,
            "category_accuracy": hits / len(group),
        }

    return {
        "records": n,
        "overall": overall,
        "per_gold_category": per_category,
        "escalation_safety": escalation,
        "calibration": calibration,
    }


def report(summary):
    """Print the summary to stdout."""
    pct = lambda d: f"{d['correct']}/{d['total']} ({d['accuracy']:.0%})"

    print("\n===== OVERALL ACCURACY =====")
    for field in ("category", "priority", "routing"):
        print(f"  {field:<9}: {pct(summary['overall'][field])}")

    print("\n===== ACCURACY PER GOLD CATEGORY =====")
    width = max((len(c) for c in summary["per_gold_category"]), default=0)
    for cat, d in summary["per_gold_category"].items():
        print(f"  {cat:<{width}} : {pct(d)}")

    print("\n===== ESCALATION SAFETY =====")
    esc = summary["escalation_safety"]
    missed, over = esc["missed_human_review"], esc["over_escalated_to_human_review"]
    print(
        f"  gold '{HUMAN_REVIEW}' -> predicted billing category : {missed['count']}"
    )
    for d in missed["detail"]:
        print(f"      {d['id']}  predicted: {d['predicted']}")
    print(
        f"  gold billing category -> predicted '{HUMAN_REVIEW}' : {over['count']}"
    )
    for d in over["detail"]:
        print(f"      {d['id']}  gold: {d['gold']}")

    print("\n===== CALIBRATION (predicted confidence vs. category accuracy) =====")
    print(f"  {'confidence':<12} {'n':>3}  {'category accuracy':>18}")
    for level, d in summary["calibration"].items():
        acc = f"{d['correct']}/{d['count']} ({d['category_accuracy']:.0%})"
        print(f"  {level:<12} {d['count']:>3}  {acc:>18}")


def main():
    parser = argparse.ArgumentParser(
        description="Score triage_v1 against the gold labels in exceptions.py."
    )
    parser.add_argument(
        "--limit", type=int, metavar="N", help="run only the first N records"
    )
    args = parser.parse_args()

    records = EXCEPTIONS
    if args.limit is not None:
        if args.limit < 1:
            parser.error("--limit must be at least 1")
        records = records[: args.limit]
    if not records:
        parser.error("no records to run")

    print(f"Running {len(records)} of {len(EXCEPTIONS)} records...\n")
    rows = run(records)
    summary = summarize(rows)
    report(summary)

    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    path = os.path.join(
        results_dir, f"run_{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    )
    payload = {
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "limit": args.limit,
        "summary": summary,
        "rows": rows,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nWrote {len(rows)} rows -> {path}")


if __name__ == "__main__":
    main()
