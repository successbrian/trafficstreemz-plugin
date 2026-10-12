# Install Guide

**Total time:** about 30 minutes if you have successbrian-os already.
About 60–90 minutes if you're starting from zero. No surprises below —
every step is spelled out.

---

## What you need

1. **successbrian-os** — this is a plugin, not a standalone app. If you
   don't have it yet: it's a free, open-source operating layer at
   https://github.com/successbrian/successbrian-os. Clone it, run its
   installer, and come back here. Budget 30–60 minutes for that if it's
   your first time.
2. **Python 3.10+** — check with `python3 --version`.
3. **A fresh Gmail account** — the installer walks you through creating
   one. This keeps your prospecting separate from your personal inbox.
4. **About 30 minutes** and your contact details (see step 2).

That's it. No paid software. No API keys. No credit card.

---

## Step-by-step

### 1. Clone the plugin (2 min)

```bash
git clone https://github.com/successbrian/trafficstreemz-plugin
cd trafficstreemz-plugin
```

### 2. Run the installer (5 min)

```bash
python3 install/onboard.py
```

The installer asks for three things: **your name, your email, your
WhatsApp.** Here's exactly what happens with them, stated before you
type anything:

- They're sent to Brian Lathe — the person who built this — so he can
  **personally help you get the system running**.
- Nothing is sent silently. The installer tells you on screen what's
  being sent and why, and asks you to confirm.
- Your details are never sold, shared, or added to a spam list. They go
  to one human for one purpose: helping you.

If you're not comfortable with that, don't install. The deal is the
deal, and it's stated up front.

### 3. Enroll in the engines (10 min)

The installer opens enrollment pages for the TrafficStreemz businesses:

- **TrafficStreemz** — Brian is pre-filled as your enroller. **You can
  change this.** Your business, your choice. The field is editable on
  screen.
- **Systeme.io** — if you don't already have an account, you'll create
  one under Brian. This powers your email funnels. Already have
  Systeme.io? Keep your account — just connect it.

### 4. Set up your Gmail (5 min)

The installer walks you through creating a dedicated Gmail account for
prospecting. Why separate? Because prospecting email and personal email
should never mix. Five minutes now saves headaches later.

### 5. Configure the prospecting engine (5 min)

The installer asks about **your** niche, **your** lists, **your**
hunting grounds. Be specific — "wellness-minded moms in Facebook
groups" beats "everyone."

Important: the plugin does **not** come with leads. It comes with the
*machine that finds leads* — from sources you point it at. Your list,
your business.

### 6. Watch the training (on your own time)

The recorded presentations (Zilara, GotBackup, My Lead Gen Secret) are
linked in the plugin. Watch them yourself first — then you'll know
exactly what to point your prospects at.

---

## You're live

```bash
python3 prospecting/finder.py --help
```

That shows everything the engine can do. Start with a small CSV of
people you already know (v0.2.0+), see the scoring work, then scale up.

---

## Troubleshooting

**`python3: command not found`** — install Python 3.10+ from
python.org, then re-run.

**Installer can't reach the lead endpoint** — check your internet
connection. Your details are also saved locally and retried — nothing
is lost.

**Something else broke** — open an issue at
https://github.com/successbrian/trafficstreemz-plugin/issues, or
message Brian on WhatsApp (he has your number now — that's the point).
Include the exact error text.

---

## What happens next

Brian follows up personally — that's the deal you agreed to in step 2.
He'll help you configure the engine, connect ContactFlowCRM, and get
your first prospect batch scored. After that, the weekly build notes at
https://successbrianhub.substack.com keep you current on what's new.
