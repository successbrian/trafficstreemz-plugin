# ContactFlowCRM ↔ Plugin Integration Contract

**Version:** 0.1.1-draft
**Status:** SPEC — implement against this when ContactFlowCRM API is ready

---

## Purpose

Define how successbrian-os plugins (starting with trafficstreemz-plugin)
exchange data with ContactFlowCRM. The CRM is the shared data layer;
plugins are the arms and legs.

## Direction 1: Plugin → CRM (lead + activity flow)

### Lead ingestion

`POST {CRM_BASE}/api/v1/leads/ingest`

```json
{
  "source_plugin": "trafficstreemz",
  "source_version": "0.1.0",
  "contact": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "whatsapp": "+15551234567"
  },
  "context": {
    "engine": "zilara",
    "signals": {"in_wellness_group": true, "engages_health_content": true},
    "score": 65,
    "score_reasons": ["+25 in_wellness_group", "+20 engages_health_content", "+20 follows_wellness_creator"]
  },
  "consent": {
    "given": true,
    "method": "plugin_installer_explicit",
    "timestamp": "2026-10-11T21:00:00Z"
  }
}
```

**CRM behavior:** dedupe on email+whatsapp; tag with
`source:trafficstreemz`, `engine:{engine}`; apply lead score; enroll in
default nurture sequence for that engine.

### Activity events (Adilo watch scoring, etc.)

`POST {CRM_BASE}/api/v1/events`

```json
{
  "contact_ref": "email:jane@example.com",
  "event": "video_watched",
  "properties": {
    "video": "zilara-247-presentation",
    "watch_pct": 87,
    "cta_clicked": "gift_card_claim"
  },
  "timestamp": "2026-10-11T21:05:00Z"
}
```

**CRM behavior:** update lead score (+/-); trigger automation rules
(e.g. watch_pct >= 80 → queue Wednesday-live invite).

## Direction 2: CRM → Plugin (automation triggers)

### Webhook: automation fired

`POST {PLUGIN_CALLBACK}/crm/automation`

```json
{
  "automation": "monthly_upgrade_invite",
  "contacts": ["email:jane@example.com"],
  "action": "send_whatsapp",
  "template": "a_to_b_invite_v1"
}
```

**Plugin behavior:** execute via the user's configured channels
(Gmail/WhatsApp); report delivery status back.

### Lead status sync

`GET {CRM_BASE}/api/v1/leads/{ref}/status` →

```json
{"stage": "customer", "tags": ["source:trafficstreemz", "engine:zilara"], "score": 72, "last_activity": "2026-10-11T21:05:00Z"}
```

**Plugin behavior:** reflect stage in local prospect views; suppress
further prospecting outreach for converted leads.

## Auth

- Plugin holds a per-install API token (issued at ContactFlowCRM
  account link step in the installer).
- All calls carry `Authorization: Bearer {token}`.
- Tokens are scoped to the installing user's ContactFlowCRM account.

## Data rules

- Consent is mandatory on every lead: no `consent.given=true`, no ingest.
- PII never logged above INFO; whatsapp numbers redacted in debug logs.
- Brian's people_unified enrichment IP never crosses this boundary —
  the contract carries only what the plugin itself collected.

## Versioning

- Contract version in `X-CRM-Contract: 0.1` header.
- Breaking changes bump minor; additive changes bump patch.
- CRM maintains N-1 compatibility.
