# Pattern 06 — States / Workflow
## Purpose
Entity has lifecycle states and allowed transitions.

## GraphQL
- Enum State
- Query by state
- Mutation transition(id,to)

## Detection
- Column `state` + transition table or code rules

## Vue
- `workflows/StatesWorkflowTabs.vue`
