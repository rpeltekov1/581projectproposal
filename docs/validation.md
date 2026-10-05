# Validation record — 2026-10-04

Passed: TypeScript compilation; production Vinext/Worker build; twelve Python unit/integration tests. Tests cover tagged-text PDF extraction, fallback requirements, authentication, persistent failed runs, idempotent successful runs, conflicting run IDs, unit conversion, unknowns, duplicate room IDs, missing-room recall, and area-basis mismatch.

Python persistence tests used temporary SQLite, not PostgreSQL. PostgreSQL container runtime was not exercised. No live model calls or MLS requests were made. No Gridsnap exports were available. Browser and WebMCP runtime validation were unavailable under the permitted preview workflow. Design PDF rendered and visually inspected. Synthetic fixture PDFs are explicitly schematic and not Gridsnap exports.

Reproduce from extraction-service: `python -m unittest discover -s tests -v`.
