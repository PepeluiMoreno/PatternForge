# Pattern 08 — Audit & Versioning
## Purpose
Track entity history (version, changedAt, changedBy, diff).

## GraphQL
- Field `history`
- Mutation `bumpVersion(id)` optional

## Detection
- History table related by entity_id

## Vue
- `workflows/AuditTimeline.vue`
