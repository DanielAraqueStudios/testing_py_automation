# libs/

Shared code used by more than one app in `../apps/`. Nx libraries, not standalone services.

Planned libs (not yet scaffolded):

- `contracts` — shared DTOs/interfaces used by both Angular and NestJS apps, so request/response
  shapes can't silently drift between a frontend and its backend service.
- `auth` — Clerk JWT verification helpers and NestJS guards shared across all backend services.
- `ui` — shared Angular components, if/when duplication across `marketing-site` and `client-portal`
  justifies it.

See [`../ARCHITECTURE.md`](../ARCHITECTURE.md) section 4 (Repository layout) for context.
