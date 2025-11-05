You will receive a canonical application model JSON (see PatternForge schema).
Your job is to generate minimal but production-grade BACKEND and FRONTEND files.

OUTPUT FORMAT (JSON only):
{
  "files": [
    {"path": "backend/schema.graphql", "content": "<SDL>"},
    {"path": "backend/resolvers.py", "content": "<python ariadne resolvers>"},
    {"path": "frontend/composables/useApi.js", "content": "<vue composable>"},
    {"path": "frontend/components/EntityList.vue", "content": "<vue component>"}
  ]
}

REQUIREMENTS:
- GraphQL: Ariadne, schema-first. Types for each entity, queries for list/detail, basic mutations (create/update/delete).
- Catalogs: generate Catalog types, queries, and seed comment.
- Resolvers: python, basic session stub (SessionLocal), TODO comments where needed.
- Vue 3: one composable per entity for list/detail; one List.vue component per entity.
- Keep code clean, English identifiers, and no external chatter.
