# Pattern 03 — One-to-Many
## Purpose
Parent owns multiple Children.

## GraphQL
- Field on Parent: {{ children_field }}: [{{ Child }}!]
- Mutations: attach (set parent_id), detach (null or delete)

## Detection
- FK on Child to Parent, not unique

## Vue
- `entities/OneToManyTable.vue`
