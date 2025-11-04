# Pattern 07 — Multimedia attachments
## Purpose
Attach files to an entity (url, mimeType, sizeBytes).

## GraphQL
- Field `attachments`
- Mutations: attach(ownerId, attachmentId), detach(...)

## Detection
- Join via 1:N or N:M

## Vue
- `multimedia/MultimediaGallery.vue`
