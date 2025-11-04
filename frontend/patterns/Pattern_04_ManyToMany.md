# Pattern 04 — Many-to-Many
## Purpose
N:M association via junction table.

## GraphQL
- Fields: {{ rights_field }} on Left, {{ lefts_field }} on Right
- Mutations: link(leftId,rightId), unlink(leftId,rightId)

## Detection
- Junction table with two FKs (PK can be composite)

## Vue
- `entities/ManyToManyManager.vue`
