# apps/

Each subfolder here is an independently deployable application (its own Railway service).
See [`../ARCHITECTURE.md`](../ARCHITECTURE.md) for the full service inventory and build order.

## Status: structural scaffold committed, not yet runnable

Every app below has a hand-rolled minimal skeleton (`package.json`, `tsconfig.json`, `src/`,
and a `prisma/schema.prisma` where the service owns a database) but **no `node_modules` has been
installed and no app has been run**. Nx/Angular-CLI generators were skipped for this pass because
`typescript@latest` (`7.0.2`) isn't yet compatible with the `@nx/angular`/`@nx/nest` tooling
available when this was scaffolded — every `package.json` pins `typescript@^5.9.0` instead.

| App | Stack | Own DB? | Status |
|---|---|---|---|
| `marketing-site` | Angular 18.2 (SSR) | — | Skeleton: landing page placeholder component |
| `client-portal` | Angular 18.2 | — (calls APIs) | Skeleton: dashboard shell + Clerk auth guard stub (not implemented) |
| `api-gateway` | NestJS | — | Skeleton: `GET /health`, TODO for Clerk/service-JWT guard |
| `quotes-service` | NestJS + Prisma | ✅ Postgres | Skeleton: `Client`/`Quote`/`QuoteService` schema (mirrors `../legacy/generate_quote.py`'s service set) |
| `crm-service` | NestJS + Prisma | ✅ Postgres | Skeleton: `Contact`/`Lead`/`Deal` schema (`Deal.progress` backs the client-portal progress view) |
| `campaigns-service` | NestJS + Prisma + BullMQ | ✅ Postgres | Skeleton: `Campaign`/`EmailTemplate`/`CampaignRecipient` schema + queue module stub |
| `ingestion-service` | NestJS + Prisma | ✅ Postgres | Skeleton: `IngestEvent` + `OutboxEvent` schema (outbox pattern, see `../ARCHITECTURE.md` §5–6) |
| `notifications-service` | NestJS | Redis (queue only) | Skeleton: WebSocket gateway stub for live chat/progress push |

## Next steps (Phase 1, per `../ARCHITECTURE.md` §7)

To make `quotes-service` + `client-portal` actually runnable:

1. `npm install` inside each app (no root-level install exists yet — each app is currently
   self-contained).
2. Stand up a Postgres instance per data-owning service and fill in its `.env` from the
   `.env.example` already present in each service folder.
3. Run Prisma generate/migrate against that database.
4. Port the real quote-generation logic from `../legacy/generate_quote.py` into
   `quotes-service`.
5. Wire real Clerk JWT verification into `client-portal`'s `app/auth/auth.guard.ts` and
   `api-gateway`'s guard (both are currently stubs).

Do not start a later-phase service (`crm-service` onward) until `quotes-service` +
`client-portal` are deployed and their API contract (see `../libs/contracts`) is stable.
