# Pattern 10 — Internationalization
## Purpose
Field translations per locale.

## GraphQL
- `translations(locale)` on entity
- Mutation `upsertTranslation(entityId, locale, input)`

## Detection
- translation table per entity or polymorphic

## Vue
- `entities/I18nTabs.vue`
