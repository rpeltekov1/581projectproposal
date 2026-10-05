# Parcel — property visualization and floor-plan intake

React / Leaflet / Chart.js prototype with a separate Python FastAPI extraction service. The Site stores its app records in D1 and originals in R2; the Python service uses PostgreSQL. **The Site is not a completed all-PostgreSQL deployment.**

## Delivered
- Filtered property map and detail sheet; derived market summaries; clearly illustrative trend series.
- Platform sign-in, server-enforced agent/client permissions, owner-scoped private plan access.
- Durable PDF/PNG/JPEG intake; retained failed/successful attempts; independent review revisions and publication.
- Original-output accuracy scoring with hashed keys and immutable score records.
- FastAPI PDF text-first extractor, vision fallback adapter, strict JSON validation and persistent run logs.
- Three-tier synthetic smoke fixtures, frozen hash manifest, evaluation CLI, 12 automated tests.
- Complete design and limitations: [design source](docs/software-design.md) and [PDF](public/software-design.pdf).

## Important boundaries
No MLS feed, real Gridsnap dataset, live vision model call or external Python deployment is included. The demonstration result is a deliberately imperfect fixed fixture, **not an AI extraction**. The tagged parser reads explicit inventory text only; it does not infer arbitrary PDF geometry. PostgreSQL listing/review models are present but hosted business operations remain in D1. Read the design's requirement/status and operations sections before widening access.

## Web application
Node 22.13+ is required. Use the checked-in pnpm lockfile with pnpm 11.25.0.

```sh
pnpm install --frozen-lockfile
pnpm run dev
```

Sites deployment uses `.openai/hosting.json`, D1/R2 bindings and generated Drizzle migrations. Hosted authentication belongs to Sites; local managed previews do not simulate a user. The first signed-in user of this **owner-private** Site bootstraps as agent; later users are clients. Replace bootstrap with an explicit membership/allowlist process before broader sharing. Do not expose a standalone dev server to untrusted traffic: forwarded platform identity headers must be trusted only behind the authenticated Sites boundary.

## Python service with PostgreSQL
Set strong values in your shell; do not commit credentials.

```sh
export POSTGRES_PASSWORD='replace-with-a-long-random-password'
export SERVICE_TOKEN='replace-with-a-long-random-service-token'
docker compose up --build
```

The service is at `http://127.0.0.1:8000`; bearer authentication is required even for `/health`. Compose persists PostgreSQL and source files. `DB_AUTO_CREATE=1` is development-only; use versioned migrations in production.

For a virtual environment:

```sh
cd extraction-service
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
# Configure DATABASE_URL, DB_AUTO_CREATE, UPLOAD_DIR and SERVICE_TOKEN.
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Ordinary plans need `VISION_API_KEY` and `VISION_MODEL`. `VISION_BASE_URL` defaults to the OpenAI-compatible endpoint. Use a vision model supporting strict JSON schema and the request settings in `app/extractor.py`; model selection is deliberately explicit. Secrets never enter the browser. A complete tagged fixture can be parsed without a model.

Deploy the Python container to your chosen HTTPS host, then configure Site secrets `EXTRACTION_SERVICE_URL` and `EXTRACTION_SERVICE_TOKEN`. Set the Python host's `SERVICE_REVISION` to the Git commit. The Site does not host Python and cannot call a localhost service.

## Tests and evaluation
```sh
cd extraction-service
python -m unittest discover -s tests -v
python evaluate.py fixtures/manifest.json --output evaluation-report.json
```

The first command uses a temporary SQLite test database; PostgreSQL deployment must be tested separately. The second requires a running authenticated service and `SERVICE_TOKEN`. Without vision settings, tagged succeeds and labelled/bare fail honestly. Failures remain in the report denominator. This one-layout synthetic set is not a Gridsnap benchmark. Supply actual Gridsnap exports and independently verified truth, confirm their schema, split by source building, and freeze the manifest before reporting model accuracy.

## Source and test artifact integrity
Run `scripts/make-fixtures.py` only when intentionally creating a new fixture version: generated PDFs receive new hashes, and the manifest must be frozen again. Never regenerate fixtures mid-comparison. `scripts/render-design.py` produces the design PDF. ReportLab is an authoring dependency, not a service dependency.

## Attribution
Photo: Waterthedog, public domain, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Waller_Street_Painted_Ladies,_San_Francisco.jpg). OpenStreetMap is credited on the map. Photos, addresses, market history, and sample agents are illustrative.
