# Pattern 01 — Catalog
## Purpose
Simple lookup table (id, optional code, name). Used by many entities via FK.

## GraphQL (SDL, schema-first)
- Query: list, get by id
- Mutations: create, update, delete
- Input: {{ Entity }}Input { {% if code_field %}{{ code_field }}: String{% endif %} name: String! }

## Detection rule (generator)
- Table has small, stable rows (<= few thousands), mainly referenced by other tables
- Required fields: id, name; optional code field

## Vue mapping
- `entities/CatalogList.vue`, `entities/CatalogModal.vue`
