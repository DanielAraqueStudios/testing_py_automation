# warehouse/

The analytical datawarehouse — a Postgres database that is a **read target for analytics only**.

- Populated by outbox consumers from the operational services in `../apps/`, never written to
  directly by any frontend.
- No app queries this database directly for user-facing requests; it exists for cross-service
  analytics/reporting.
- Schema and migrations will live in `warehouse/prisma/` once Phase 4 (see `../ARCHITECTURE.md`)
  begins.

Not yet scaffolded.
