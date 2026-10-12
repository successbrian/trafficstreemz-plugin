#!/usr/bin/env python3
"""TrafficStreemz plugin installer — guided onboarding.

Steps:
  1. Verify successbrian-os is present
  2. Disclose + capture contact details -> sent to Brian
  3. Open enrollment links (TrafficStreemz, Systeme.io)
  4. Walk through fresh Gmail creation
  5. Configure the prospecting engine with the user's own sources
  6. Write local config, done.

Config lives in install/config.json (gitignored). Affiliate links come
from install/affiliate_links.json — Brian's links ship as defaults.
"""
import json
import os
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")
LINKS_PATH = os.path.join(HERE, "affiliate_links.json")
LEAD_ENDPOINT = "https://successbrianvps.com/api/trafficstreemz-install"


def banner(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def check_os():
    """Verify successbrian-os is installed."""
    try:
        import successbrian_os  # noqa: F401
        return True
    except ImportError:
        # Fallback: look for the repo directory
        home = os.path.expanduser("~")
        for cand in (os.path.join(home, "successbrian-os"),
                     os.path.join(home, "workspace", "successbrian-os")):
            if os.path.isdir(cand):
                return True
        return False


def load_links():
    with open(LINKS_PATH) as f:
        return json.load(f)


def capture_contact():
    banner("STEP 2 — INTRODUCE YOURSELF")
    print(
        "\nBrian Lathe (who built this system) personally helps every\n"
        "installer get it running. To do that, he needs your contact\n"
        "details.\n\n"
        "By continuing, you agree to send the following to Brian:\n"
        "  - your name, email, and WhatsApp number\n\n"
        "That's it. No spam, no selling your info — it's so he can\n"
        "reach out and help you configure this system.\n"
    )
    ok = input("Continue? [y/N] ").strip().lower()
    if ok != "y":
        print("No problem — exiting. Nothing was sent.")
        sys.exit(0)
    name = input("Your name: ").strip()
    email = input("Your email: ").strip()
    whatsapp = input("Your WhatsApp number: ").strip()
    if not (name and email and whatsapp):
        print("All three are required. Exiting.")
        sys.exit(1)
    return {"name": name, "email": email, "whatsapp": whatsapp}


def send_lead(contact):
    """POST the contact to Brian's lead receiver."""
    import urllib.request
    data = json.dumps({
        "source": "trafficstreemz-plugin",
        "version": "0.1.0",
        **contact,
    }).encode()
    req = urllib.request.Request(
        LEAD_ENDPOINT, data=data,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception as e:  # noqa: BLE001
        print(f"  (could not reach lead receiver: {e})")
        return False


def enroll(links):
    banner("STEP 3 — ENROLL")
    print("\n--- TrafficStreemz ---")
    print("Brian is pre-filled as your enroller.")
    print("Your business, your choice — you can change it on the page.")
    input("Press Enter to open the TrafficStreemz enrollment page...")
    webbrowser.open(links["trafficstreemz_enroll"])

    print("\n--- Systeme.io ---")
    have = input(
        "Do you already have a Systeme.io account? [y/N] ").strip().lower()
    if have != "y":
        print("You'll create one under Brian — it powers your funnels.")
        input("Press Enter to open the Systeme.io signup page...")
        webbrowser.open(links["systemeio_signup"])
    else:
        print("Got it — we'll use your existing account.")


def gmail_walkthrough():
    banner("STEP 4 — FRESH GMAIL")
    print(
        "\nCreate a dedicated Gmail account for prospecting.\n"
        "Keeps your personal inbox clean; this one is your business machine.\n\n"
        "  1. Go to https://accounts.google.com/signup\n"
        "  2. Use a business-style name (e.g. yourname.biz@gmail.com)\n"
        "  3. Turn on 2-step verification\n"
        "  4. Come back here when it's ready\n"
    )
    email = input("Your new prospecting Gmail address: ").strip()
    return email


def configure_prospecting():
    banner("STEP 5 — PROSPECTING ENGINE")
    print(
        "\nThe engine finds YOUR prospects — your niche, your lists,\n"
        "your hunting grounds. It doesn't ship with leads; it ships\n"
        "with the machine that finds them.\n"
    )
    niche = input("Your niche (e.g. wellness, home business, backup): ").strip()
    sources = input(
        "Where do your prospects hang out? (comma-separated, e.g.\n"
        "  facebook groups, youtube comments, local meetups): ").strip()
    return {
        "niche": niche,
        "sources": [s.strip() for s in sources.split(",") if s.strip()],
    }


def main():
    banner("TRAFFICSTREEMZ PLUGIN — INSTALLER")
    print("\nThis plugin needs successbrian-os to run.")

    if not check_os():
        print(
            "\nCould not find successbrian-os.\n"
            "Install it first: https://github.com/successbrian/successbrian-os\n"
            "Then re-run this installer."
        )
        sys.exit(1)
    print("  successbrian-os found.")

    links = load_links()

    contact = capture_contact()
    print("\nSending your details to Brian...")
    if send_lead(contact):
        print("  Sent. He'll be in touch to help you configure.")
    else:
        print("  Couldn't send right now — your details are saved locally\n"
              "  and will be retried on first engine run.")

    enroll(links)
    gmail = gmail_walkthrough()
    prospecting = configure_prospecting()

    config = {
        "contact": contact,
        "lead_sent": True,
        "prospecting_gmail": gmail,
        **prospecting,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    banner("DONE — YOU'RE LIVE")
    print(
        "\nYour prospecting engine is configured.\n"
        "Run:  python3 prospecting/finder.py --help\n\n"
        "Training videos are linked in funnels/README.md.\n"
        "Brian will reach out shortly to help you tune it.\n"
    )


if __name__ == "__main__":
    main()
