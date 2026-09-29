# Sistema de Cotizaciones — Platform

A multi-service SaaS ecosystem for quoting, client management, and lifecycle automation — evolving
from a single-purpose Python desktop quote generator into an independently-deployed platform of
Angular/NestJS services on Railway, backed by a shared analytical datawarehouse.

**Start here:** [`ARCHITECTURE.md`](./ARCHITECTURE.md) — full service inventory, data flow diagrams,
security model, and phased build order. This README is the orientation layer; ARCHITECTURE.md is the
source of truth for implementation decisions.

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | **Angular 18** (SSR for the public site, SPA for the portal) | Team's existing framework expertise; SSR needed for marketing-site SEO. |
| Backend | **NestJS** | Modular, dependency-injection-first, integrates cleanly with Prisma and guards/interceptors for cross-cutting auth. |
| ORM / Database | **Prisma + PostgreSQL**, one database per service | Strict service isolation — no service is ever handed another service's connection string. |
| Auth (user-facing) | **Clerk** (JWT) | Managed auth avoids hand-rolling session/password infra for the client portal. |
| Auth (service-to-service) | Short-lived internal JWTs, client-credentials style | Keeps inter-service calls authenticated without sharing user credentials or databases. |
| Queueing | **BullMQ + Redis** (campaigns-service) | Reliable job queue for email sending sequences. |
| Real-time | **WebSocket gateway** (Socket.IO, notifications-service) + managed chat SDK | Live chat and progress push without building chat infra from scratch. |
| Automation / AI | **n8n** (self-hosted on Railway) | Visual workflow automation for the AI assistant bot, without a bespoke orchestration service. |
| Monorepo tooling | **Nx** (apps/ + libs/ layout) | Shared TypeScript DTOs between Angular and NestJS without duplicating types, while each app still deploys independently. |
| Hosting | **Railway**, one deployment + one database per service | Matches the "independent service, independent DB" architecture principle below. |
| Language | **TypeScript** everywhere in the new platform (pinned `^5.9.x`) | Type-safety shared across `libs/contracts` on both frontend and backend. |
| Legacy | **Python 3 / PyQt6** (`legacy/`) | The original desktop quote generator — kept functional as the Phase 1 porting reference, not part of the new platform runtime. |

## Architecture principles

1. **One service, one database.** Every data-owning app in `apps/` has its own Postgres instance. No
   service ever receives credentials to another service's database — cross-service reads happen only
   through that service's API.
2. **Independent deployability.** Each folder under `apps/` is a separate Railway deployment. A service
   can be redeployed, scaled, or rolled back without touching any other service.
3. **JWT-based trust boundary, not network trust.** Every request — user-facing or internal — carries a
   verifiable JWT. `api-gateway` verifies Clerk-issued user JWTs; internal calls carry short-lived
   service-to-service JWTs. No service trusts a caller based on network location alone.
4. **Outbox over dual-writes.** Anything that must reach the shared datawarehouse is written via an
   outbox table in the owning service's own database, then relayed — never written synchronously to two
   databases in the same request, which risks silent drift if the second write fails.
5. **Shared contracts, not shared runtime.** `libs/contracts` gives Angular and NestJS apps the same
   DTO/interface definitions at build time. It is a compile-time dependency only — it never becomes a
   shared running process or a coupling point between deployments.
6. **Phased build order, contract-first.** A later-phase service is not started until the earlier
   phase's service is deployed and its API contract (defined in `libs/contracts`) is stable. See
   `ARCHITECTURE.md` §7 for the full phase breakdown.
7. **Nothing historical is deleted.** The pre-refactor Python tool, legal/registration documents, and
   prior research material are preserved under `legacy/` as reference and as the functional baseline
   Phase 1 is ported from — not wiped in favor of the rewrite.

## Repository layout

```
apps/       # Independently deployable services (Angular/NestJS) — see apps/README.md
libs/       # Shared Nx libraries (contracts, auth, ui) — see libs/README.md
warehouse/  # Analytical Postgres datawarehouse — see warehouse/README.md
legacy/     # The original Python desktop tool + legal/registration docs
ARCHITECTURE.md   # Full platform architecture — read this first
CLAUDE.md         # Ruflo / Claude Code project configuration
```

### `apps/` — services

| App | Stack | Own DB? | Role |
|---|---|---|---|
| `marketing-site` | Angular (SSR) | — | Public site, service catalog, lead capture |
| `client-portal` | Angular | — (calls APIs) | Authenticated dashboard: project progress, live chat |
| `api-gateway` | NestJS | — | Single entry point; Clerk JWT verification, routing |
| `quotes-service` | NestJS + Prisma | ✅ Postgres | Quote generation, ported from `legacy/generate_quote.py` |
| `crm-service` | NestJS + Prisma | ✅ Postgres | Leads, deals, pipeline, client lifecycle |
| `campaigns-service` | NestJS + Prisma + BullMQ | ✅ Postgres | Email sequences, sending queue |
| `ingestion-service` | NestJS + Prisma | ✅ Postgres | External webhooks/data intake, outbox producer |
| `notifications-service` | NestJS + WebSocket gateway | Redis (queue only) | Live chat transport, progress push |

See [`apps/README.md`](./apps/README.md) for current scaffold status per app.

### `libs/` — shared code

| Lib | Purpose |
|---|---|
| `contracts` | Shared DTOs/interfaces used by both Angular and NestJS apps |
| `auth` | Clerk JWT verification helpers, service-to-service JWT guards |
| `ui` | Shared Angular components |

See [`libs/README.md`](./libs/README.md).

### `warehouse/`

Analytical Postgres database, populated by outbox consumers from the operational services — never
written to directly by any frontend, and not queried directly for user-facing requests. See
[`warehouse/README.md`](./warehouse/README.md).

### `legacy/`

The pre-refactor codebase, preserved rather than deleted:

- `generate_quote.py`, `quote_gui.py`, `run_gui.py`, `test_gui.py` — the Python/PyQt6 quote generator
  (console + GUI).
- `template.html`, `index.html`, `ORIGINAL ONE.html`, `assets/` — the HTML quote template and static
  assets.
- `cotizaciones/` — generated per-client quote output from past runs.
- `ejecutable/`, `ejecutable.rar` — the packaged Windows executable/installer.
- `generar_documentos_legales.py`, `registro_legal_colombia/` — Colombian software legal-registration
  document generator and its output.

Still functional as-is; see [`legacy/README_quote_generator.md`](./legacy/README_quote_generator.md)
for how to run it. Nothing here is deleted or modified as part of the platform refactor — it's the
reference material and functional baseline `quotes-service` (Phase 1) is ported from.

## Status

`apps/`, `libs/`, `warehouse/` are **structural scaffolding only** — hand-rolled skeletons (package.json,
tsconfig, Prisma schemas where applicable) with no dependencies installed and no service running yet.
See `apps/README.md` for the current per-service scaffold table and the concrete Phase 1 next steps.

## Build order

Full phase breakdown lives in [`ARCHITECTURE.md`](./ARCHITECTURE.md) §7:

0. Skeleton — Nx-style workspace layout, `api-gateway`, Clerk integration, `libs/contracts`.
1. **Current target phase** — `quotes-service` + `client-portal` runnable end-to-end.
2. CRM — `crm-service`, lead capture, real project status in the portal.
3. Campaigns + Notifications — `campaigns-service`, live chat.
4. Warehouse + Ingestion — outbox rollout, `warehouse` schema, `ingestion-service`.
5. AI Assistant — n8n deployment wired to CRM/campaigns events.

## Contributing / commit conventions

Conventional commits (`feat`, `fix`, `chore`, `docs`, `refactor`), one logical change per commit, scoped
to the app/lib touched (e.g. `feat(quotes-service): ...`). No secrets, `.env` files, or Ruflo/Claude Code
tooling artifacts are ever committed — see `.gitignore`.
