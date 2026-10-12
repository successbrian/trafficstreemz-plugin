#!/usr/bin/env python3
"""Prospect finder — v0.1.0 scaffold.

Loads the installer's config, applies per-engine prospect profiles,
and provides the scoring + source interface that v0.2.0 connectors
will plug into.

Usage:
    python3 prospecting/finder.py --help
    python3 prospecting/finder.py --engine zilara --list-sources
    python3 prospecting/finder.py --engine gotbackup --score <prospect.json>

v0.1.0: profiles + scoring rubric + source interface.
v0.2.0: real source connectors (group scrapers, comment miners).
Outreach stays human-reviewed until trust is earned — no auto-sending.
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.join(HERE, "..", "install")
CONFIG_PATH = os.path.join(INSTALL_DIR, "config.json")

ENGINES = ("zilara", "gotbackup", "mlgs")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("Run install/onboard.py first.")
        raise SystemExit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def score_prospect(prospect, profile):
    """Score 0-100: fit for this engine. Deterministic, explainable."""
    score = 0
    reasons = []
    signals = prospect.get("signals", {})
    weights = profile.get("signal_weights", {})
    for signal, weight in weights.items():
        if signals.get(signal):
            score += weight
            reasons.append(f"+{weight} {signal}")
    return {"score": min(score, 100), "reasons": reasons}


def main():
    ap = argparse.ArgumentParser(description="TrafficStreemz prospect finder")
    ap.add_argument("--engine", choices=ENGINES, required=True)
    ap.add_argument("--list-sources", action="store_true")
    ap.add_argument("--score", metavar="PROSPECT_JSON",
                    help="Score a prospect JSON file against the engine profile")
    args = ap.parse_args()

    config = load_config()
    profile_path = os.path.join(HERE, "profiles", f"{args.engine}.json")
    if os.path.exists(profile_path):
        with open(profile_path) as f:
            profile = json.load(f)
    else:
        profile = {"signal_weights": {}, "sources": []}

    if args.list_sources:
        print(f"Sources for {args.engine} (from your config):")
        for s in config.get("sources", []):
            print(f"  - {s}")
        for s in profile.get("sources", []):
            print(f"  - {s} (profile default)")
        return

    if args.score:
        with open(args.score) as f:
            prospect = json.load(f)
        result = score_prospect(prospect, profile)
        print(json.dumps(result, indent=2))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
