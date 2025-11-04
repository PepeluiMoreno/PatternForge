# Pattern 09 — Security (Roles / Grants)
## Purpose
Grant/revoke roles to users.

## GraphQL
- Enum Role
- Mutations: grantRole(userId,role), revokeRole(userId,role)

## Detection
- user_roles join table

## Vue
- `workflows/SecurityRolesMatrix.vue`
