# Pattern 11 — Performance / Connections
## Purpose
Relay-style pagination and sorting.

## GraphQL
- `{{ entities_connection_field }}(after, first, search, orderBy, order): Connection`

## Detection
- Large lists, indexed fields

## Vue
- `validation/PerformancePaginator.vue`
