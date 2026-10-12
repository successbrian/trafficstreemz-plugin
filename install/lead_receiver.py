#!/usr/bin/env python3
"""TrafficStreemz plugin install lead receiver.

Receives the contact capture POST from install/onboard.py and stores it
for Brian's follow-up. Deploy on the VPS behind nginx.

Endpoint: POST /api/trafficstreemz-install
Body: {"source": "trafficstreemz-plugin", "version": "...",
        "name": "...", "email": "...", "whatsapp": "..."}

Storage: PostgreSQL (ecosystem_central, table
trafficstreemz.install_leads) — falls back to a local JSONL file if the
DB is unreachable, so no lead is ever lost.

Run:  python3 lead_receiver.py  (systemd service on the VPS)
"""
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

TABLE_SQL = """
CREATE TABLE IF NOT EXISTS trafficstreemz.install_leads (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    source TEXT DEFAULT 'trafficstreemz-plugin',
    plugin_version TEXT,
    received_at TIMESTAMPTZ DEFAULT now(),
    contacted BOOLEAN DEFAULT FALSE,
    notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_install_leads_email
    ON trafficstreemz.install_leads (email);
"""

FALLBACK_PATH = "/var/log/trafficstreemz/install_leads.jsonl"


def store_lead(lead):
    """Try Postgres; fall back to JSONL so no lead is ever lost."""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ.get("PGHOST", "localhost"),
            dbname=os.environ.get("PGDATABASE", "ecosystem_central"),
            user=os.environ.get("PGUSER", "successbrian"),
        )
        cur = conn.cursor()
        cur.execute(TABLE_SQL)
        cur.execute(
            "INSERT INTO trafficstreemz.install_leads "
            "(name, email, whatsapp, source, plugin_version) "
            "VALUES (%s, %s, %s, %s, %s)",
            (lead["name"], lead["email"], lead["whatsapp"],
             lead.get("source", "trafficstreemz-plugin"),
             lead.get("version")),
        )
        conn.commit()
        cur.close()
        conn.close()
        return "postgres"
    except Exception as e:  # noqa: BLE001
        os.makedirs(os.path.dirname(FALLBACK_PATH), exist_ok=True)
        with open(FALLBACK_PATH, "a") as f:
            f.write(json.dumps({
                **lead,
                "received_at": datetime.now(timezone.utc).isoformat(),
                "fallback_reason": str(e),
            }) + "\n")
        return "jsonl-fallback"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        if self.path != "/api/trafficstreemz-install":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            lead = json.loads(self.rfile.read(length))
        except Exception:  # noqa: BLE001
            self.send_response(400)
            self.end_headers()
            return
        if not all(lead.get(k) for k in ("name", "email", "whatsapp")):
            self.send_response(422)
            self.end_headers()
            self.wfile.write(b'{"ok": false, "error": "name, email, whatsapp required"}')
            return
        where = store_lead(lead)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "stored": where}).encode())

    def log_message(self, *args):  # noqa: D102
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5057"))
    print(f"trafficstreemz lead receiver on :{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
