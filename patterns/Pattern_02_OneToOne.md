# Pattern 02 — One-to-One
## Purpose
Exclusive 1:1 relationship between Parent and Child.

## GraphQL
- Field on Parent: {{ child_field }}: {{ Child }}
- Mutations: link, unlink

## Detection
- Unique FK from Child to Parent

## Vue
- `entities/OneToOneCard.vue`
