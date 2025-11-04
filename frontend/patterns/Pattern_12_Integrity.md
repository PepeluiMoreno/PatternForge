# Pattern 12 — Integrity & Validation
## Purpose
Uniqueness and reference checks as mutations.

## GraphQL
- `validateUnique(field1:..., field2:...)`
- `validateReference(field, value, reference, referenceField)`

## Detection
- Unique constraints, FK existence

## Vue
- `validation/IntegrityValidationForm.vue`
