# Sistema de Cotizaciones — Platform Architecture (Developer Guide)

> Status: **Design / pre-implementation**. This document describes the target architecture for the
> refactor from a single Python desktop script into a multi-service SaaS ecosystem. Nothing described
> here exists in code yet unless explicitly marked `[EXISTING]`.

## 1. Why this refactor

The current system `[EXISTING]` is a Python/PyQt6 desktop tool (`generate_quote.py`, `quote_gui.py`)
that generates one HTML quote per run and writes it to `cotizaciones/<client>/to_upload/`. It has no
persistence, no auth, no API, and no way to track a client relationship beyond the quote file itself.

The target system treats "generate a quote" as **one function of a larger commercial platform**:
marketing site → lead capture (CRM) → quote → client portal (progress + live chat) → email campaigns →
company-wide analytics (datawarehouse) → AI-assisted automation (n8n). Each of those is a separate,
independently deployable service.

## 2. Decisions already made

| Decision | Choice | Rationale |
|---|---|---|
| Repo strategy | **Nx monorepo** | Shared TypeScript contracts (DTOs) between Angular and NestJS services without duplicating types; each app still deploys independently. |
| Frontend | **Angular** | User's existing preference / team skill. |
| Backend | **NestJS** | User's existing preference; modular, DI-friendly, pairs well with Prisma. |
| ORM / DB | **Prisma + PostgreSQL**, one database per service | Service isolation — no service reaches into another's schema. |
| Auth | **Clerk** (JWT-based) | Avoid hand-rolling session/auth infra for the client portal; issues JWTs NestJS services verify. |
| Live chat | **Managed chat SDK** (e.g. Stream Chat), not hand-built | Less undifferentiated infra to maintain. |
| AI assistant | **n8n**, not a custom orchestration service | Visual workflow tool matches "AI assistant bot" requirement without building a bespoke orchestrator. |
| Hosting | **Railway**, one deployment per service | Matches "each service will have its own deployment and database." |
| Cross-service data sharing | **Internal API calls with service-to-service JWTs**, never direct cross-database access | Keeps services loosely coupled and independently deployable. |
| Analytics | **Datawarehouse (Postgres)** fed via an **outbox/event pattern**, not synchronous dual-writes | Avoids write coupling between operational services and analytics. |

Open / not yet decided: message broker choice (Redis+BullMQ vs NATS/RabbitMQ), monorepo tool version
pinning, object storage provider for generated quote HTML/PDF (Cloudflare R2 vs Railway volumes).

## 3. Service inventory

| Service | Stack | Own DB? | Responsibility |
|---|---|---|---|
| `apps/marketing-site` | Angular (SSR) | — | Public site, service catalog, lead capture forms |
| `apps/client-portal` | Angular | — (calls APIs) | Authenticated dashboard: project progress, live chat |
| `apps/api-gateway` | NestJS | — | Single entry point; auth enforcement, routing, rate limiting |
| `apps/quotes-service` | NestJS + Prisma | ✅ Postgres | Quote generation (ported from `generate_quote.py` logic), HTML/PDF export |
| `apps/crm-service` | NestJS + Prisma | ✅ Postgres | Leads, deals, pipeline, client lifecycle ("internal Salesforce") |
| `apps/campaigns-service` | NestJS + Prisma + BullMQ | ✅ Postgres | Email sequences, sending queue |
| `apps/ingestion-service` | NestJS + Prisma | ✅ Postgres (or writes straight to warehouse) | Webhooks/external data intake |
| `apps/notifications-service` | NestJS + WebSocket gateway | Redis (queue only) | Live chat transport, push notifications for progress updates |
| `warehouse` | Postgres (analytical) | ✅ | Cross-service analytics; populated by outbox consumers, never written to directly by frontends |
| `n8n` (external) | n8n self-hosted on Railway | — | AI assistant workflows, automation triggers (new lead → CRM → email) |

Each `apps/*-service` NestJS app owns exactly one Prisma schema and one Postgres database on Railway.
No service is ever given credentials to another service's database.

## 4. Repository layout (target)

```
/                                   # Nx workspace root
├── apps/
│   ├── marketing-site/             # Angular
│   ├── client-portal/              # Angular
│   ├── api-gateway/                # NestJS
│   ├── quotes-service/             # NestJS + Prisma
│   ├── crm-service/                # NestJS + Prisma
│   ├── campaigns-service/          # NestJS + Prisma
│   ├── ingestion-service/          # NestJS + Prisma
│   └── notifications-service/      # NestJS
├── libs/
│   ├── contracts/                  # Shared DTOs/interfaces used by both Angular & NestJS apps
│   ├── auth/                       # Clerk JWT verification helpers, shared guards
│   └── ui/                         # Shared Angular components (if/when needed)
├── warehouse/
│   └── prisma/                     # Analytical schema + migration scripts
├── legacy/                         # Current Python system + legal/poster docs, preserved as-is
│   ├── generate_quote.py
│   ├── quote_gui.py
│   ├── registro_legal_colombia/
│   └── semillero_investigacion/
├── nx.json
├── package.json
└── ARCHITECTURE.md                 # this file
```

`legacy/` exists so the current working Python tool, the legal registration docs, and the research
poster are not lost or scattered during the migration — they are historical/reference material, not
part of the new platform's runtime.

## 5. Data flow (representative request)

**Client views project progress in the portal:**

1. Browser → `client-portal` (Angular) — user is authenticated via Clerk, holds a JWT.
2. `client-portal` calls `api-gateway` with the JWT in `Authorization: Bearer`.
3. `api-gateway` verifies the JWT (Clerk public key) and forwards the request to `crm-service`
   (which owns "project status") with a **short-lived internal service JWT** identifying the gateway.
4. `crm-service` returns project status from its own Postgres DB.
5. For live chat, `client-portal` opens a WebSocket to `notifications-service` directly (not through
   the gateway's HTTP path), authenticated the same way.

**New lead → CRM → warehouse (event flow):**

1. `marketing-site` submits a lead form → `ingestion-service`.
2. `ingestion-service` validates and writes the lead to its own DB, then writes a domain event
   (`lead.created`) to its **outbox table**.
3. A worker (poller or listener) reads the outbox and (a) calls `crm-service` to create the lead record,
   and (b) publishes the same event to the `warehouse` ingestion pipeline.
4. `crm-service` and `warehouse` never talk to `ingestion-service`'s database directly — only through
   its API / the event it emitted.

## 6. Cross-service security model

- **User-facing auth:** Clerk issues JWTs to the browser; every service verifies them via Clerk's
  public JWKS. No service stores passwords.
- **Service-to-service auth:** short-lived JWTs issued by a trusted internal issuer (client-credentials
  style), scoped per calling service. A service must never accept a user JWT as proof of another
  service's identity.
- **No shared databases.** If `crm-service` needs quote data, it calls `quotes-service`'s API — it does
  not get a connection string to the quotes database.
- **Outbox pattern** for anything that must reach the warehouse, to avoid dual-write failures (e.g. DB
  write succeeds, event publish fails, warehouse silently drifts).

## 7. Build order (phased)

This is a large surface area; build incrementally, validating each phase before starting the next.

1. **Phase 0 — Skeleton:** Nx workspace, `api-gateway`, Clerk integration, shared `libs/contracts`.
2. **Phase 1 — Quotes + Portal:** port `generate_quote.py` logic into `quotes-service`
   (NestJS + Prisma), build `client-portal` (Angular) with Clerk auth and a basic progress view.
3. **Phase 2 — CRM:** `crm-service`, lead capture on `marketing-site`, portal shows real project status.
4. **Phase 3 — Campaigns + Notifications:** `campaigns-service`, live chat via managed SDK in
   `notifications-service`.
5. **Phase 4 — Warehouse + Ingestion:** outbox pattern rollout across services, `warehouse` schema,
   `ingestion-service` for external data.
6. **Phase 5 — AI Assistant:** n8n deployment, workflows wired to CRM/campaigns events.

Do not start a later phase's service until the prior phase's service is deployed and its API contract
is stable — later services depend on those contracts.

## 8. What "done" looks like for Phase 1 (first slice)

- [ ] Nx workspace scaffolded, `api-gateway` and `quotes-service` deploy independently on Railway.
- [ ] `quotes-service` has its own Postgres DB via Prisma; quote generation logic matches
      `legacy/generate_quote.py` output (functional parity, not the exact HTML template necessarily).
- [ ] `client-portal` authenticates via Clerk and can call `api-gateway` → `quotes-service`.
- [ ] `libs/contracts` defines the DTOs used by both `client-portal` and `quotes-service`.
- [ ] No service holds another service's DB credentials.

## 9. Open questions for the next design pass

- Message broker: Redis+BullMQ (simpler, sufficient for campaigns queue) vs NATS/RabbitMQ (true
  pub/sub if more services need to react to the same event later)?
- Object storage for generated quote HTML/PDF: Railway volumes vs Cloudflare R2?
- Does `ingestion-service` need its own operational DB, or does it write straight to the warehouse
  and rely on `crm-service`'s API for anything transactional?
- Single Clerk organization for all client accounts, or per-client organizations/roles?
