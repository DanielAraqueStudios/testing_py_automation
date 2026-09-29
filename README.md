# Sistema de Cotizaciones — Platform

This repository is transitioning from a single Python desktop quote-generator into a multi-service
SaaS ecosystem (marketing site, client portal, CRM, campaigns, quotes, ingestion, notifications, a
shared datawarehouse, and an n8n-driven AI assistant).

**Start here:** [`ARCHITECTURE.md`](./ARCHITECTURE.md) — the full target architecture, service
inventory, data flow, security model, and phased build order.

## Repository layout

```
apps/       # Independently deployable services (Angular/NestJS) — see apps/README.md
libs/       # Shared Nx libraries (contracts, auth, ui) — see libs/README.md
warehouse/  # Analytical Postgres datawarehouse — see warehouse/README.md
legacy/     # The original Python desktop tool + legal/registration docs + research poster
ARCHITECTURE.md   # Full platform architecture (read this first)
CLAUDE.md         # Ruflo / Claude Code project configuration
```

## Status

- `apps/`, `libs/`, `warehouse/` — **scaffolding only**, not yet implemented. See each folder's
  README and `ARCHITECTURE.md` section 7 ("Build order") for what comes first.
- `legacy/` — the current, working Python system. Still functional as-is; see
  [`legacy/README_quote_generator.md`](./legacy/README_quote_generator.md) for how to run it.

## What's in `legacy/`

The pre-refactor codebase, preserved rather than deleted:

- `generate_quote.py`, `quote_gui.py`, `run_gui.py`, `test_gui.py` — the Python/PyQt6 quote
  generator (console + GUI).
- `template.html`, `index.html`, `ORIGINAL ONE.html`, `assets/` — the HTML quote template and its
  static assets.
- `cotizaciones/` — generated per-client quote output from past runs.
- `ejecutable/`, `ejecutable.rar` — the packaged Windows executable/installer.
- `generar_documentos_legales.py`, `registro_legal_colombia/` — Colombian software
  legal-registration document generator and its output (unrelated to the quoting product itself).
- `semillero_investigacion/` — academic research poster material (REDCOLSI/UMNG), documenting this
  project for a university research showcase.

Nothing in `legacy/` is deleted or modified as part of the platform refactor — it's kept as
reference material and as the functional baseline the new `quotes-service` (Phase 1) is ported from.

## Next steps

See `ARCHITECTURE.md` section 7 for the phased build order. Phase 0/1 (Nx workspace skeleton,
`api-gateway`, `quotes-service`, `client-portal`) has not started yet.
