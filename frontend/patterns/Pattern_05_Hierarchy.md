# Pattern 05 — Hierarchy
## Purpose
Tree structure (parent_id self-FK) or closure table.

## GraphQL
- Node type with `children` and `parent`
- Query roots

## Detection
- Self-FK or closure table

## Vue
- `entities/HierarchyTree.vue`
