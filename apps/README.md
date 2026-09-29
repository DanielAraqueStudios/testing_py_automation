# apps/

Each subfolder here is an independently deployable application (its own Railway service).
See [`../ARCHITECTURE.md`](../ARCHITECTURE.md) for the full service inventory and build order.

Planned apps (not yet scaffolded):

- `marketing-site` — Angular (SSR) public site
- `client-portal` — Angular client dashboard (Clerk auth, progress tracking, live chat)
- `api-gateway` — NestJS entry point, auth enforcement, routing
- `quotes-service` — NestJS + Prisma, ports the logic in `../legacy/generate_quote.py`
- `crm-service` — NestJS + Prisma, lead/deal pipeline
- `campaigns-service` — NestJS + Prisma + BullMQ, email automation
- `ingestion-service` — NestJS + Prisma, external data intake
- `notifications-service` — NestJS, WebSocket gateway for live chat/progress push

Build order: see "Phased build order" in `../ARCHITECTURE.md`. Phase 1 starts with
`quotes-service` + `client-portal`.
