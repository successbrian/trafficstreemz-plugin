# Prospecting Engine

The engine that turns this plugin from a download into a business.

## Philosophy

It does NOT ship with leads. It ships with the **machine that finds
leads** — configured around *your* niche and *your* hunting grounds.

Brian's own prospect database stays private. This engine gives every
installer their own prospecting capability, which is more valuable
anyway: a list goes stale, a machine keeps producing.

## How it works

`finder.py` is the entry point. Profiles per engine:

- **Zilara** — wellness-minded prospects (health groups, wellness
  creators, supplement audiences)
- **GotBackup** — anyone with a phone full of photos and no backup
  (parents, creators, small businesses)
- **My Lead Gen Secret** — aspiring email marketers, affiliate beginners

Each profile defines: where to look, what to say first, and how to
qualify. The engine scores and ranks; you (or your Gmail automation)
start conversations.

## Profiles

Profiles live in `prospecting/profiles/` (one JSON per engine).
Copy `zilaria.example.json` to start.

## Honest limits (v0.1.0)

- `finder.py` is a scaffold: profile loading, scoring rubric, and a
  pluggable source interface. Real source connectors (group scrapers,
  comment miners) land in v0.2.0.
- Outreach is templates + Gmail drafts in v0.1.0 — no auto-sending.
  You review, you hit send. Automation comes after trust is earned.
