# Deploy MindsDB on Fly.io (BrightforestX)

This directory contains a production Fly.io layout for the BrightforestX MindsDB fork: **region `iad`**, **scale-to-zero** (`min_machines_running = 0` with Fly Proxy autostop/autostart), and a persistent volume for MindsDB storage.

The image is built from the existing `docker/mindsdb.Dockerfile` **`fly`** target (HTTP API on port **47334**, Studio disabled).

> **Do not** add a `buzz-stack-wake-proxy` app here. Wake/proxy for the ontology stack already lives on **ontology-stack**; this app relies on Fly’s built-in `auto_start_machines` for cold starts (~2s+).

## Prerequisites

- [Fly CLI](https://fly.io/docs/flyctl/install/) installed and logged in (`fly auth login`)
- Fly org access to create apps in **`iad`**
- No secrets committed to git — set them with `fly secrets set`

## One-time setup

From the **repository root**:

```bash
# 1) Create the app (pick a globally unique name; update deploy/fly/fly.toml `app` to match)
fly apps create mindsdb-lighthouse-bay --org <your-org>

# 2) Volume for MindsDB metadata/models (one volume per app in iad)
fly volumes create mdb_storage --region iad --size 1 --app mindsdb-lighthouse-bay

# 3) Required secrets (customer-facing: always enable HTTP auth)
fly secrets set \
  MINDSDB_USERNAME='<service-user>' \
  MINDSDB_PASSWORD='<strong-password>' \
  --app mindsdb-lighthouse-bay
```

### Optional secrets

| Secret | Purpose |
|--------|---------|
| `MINDSDB_DB_CON` | External Postgres URL for MindsDB system DB (recommended for production instead of SQLite on the volume) |
| `MINDSDB_DEFAULT_PROJECT` | Default project name (lowercase) |
| `MINDSDB_LOG_LEVEL` | e.g. `INFO`, `DEBUG` |
| `MINDSDB_ML_QUEUE_*` | Redis-backed ML task queue (see `mindsdb/utilities/config.py`) |

Example optional Postgres:

```bash
fly secrets set MINDSDB_DB_CON='postgresql://user:pass@host:5432/mindsdb' --app mindsdb-lighthouse-bay
```

Attach Fly Postgres if you use it:

```bash
fly postgres attach --app mindsdb-lighthouse-bay <postgres-app-name>
# Then set MINDSDB_DB_CON from the generated DATABASE_URL if needed
```

## Deploy

From the **repository root** (build context must be the repo root):

```bash
fly deploy --config deploy/fly/fly.toml --app mindsdb-lighthouse-bay
```

Verify:

```bash
curl -fsS "https://mindsdb-lighthouse-bay.fly.dev/api/util/ping"
# {"status":"ok"}
```

With HTTP auth enabled (after secrets are set):

```bash
curl -fsS -u "$MINDSDB_USERNAME:$MINDSDB_PASSWORD" \
  "https://mindsdb-lighthouse-bay.fly.dev/api/util/ping"
```

## Public URL shape (lighthouse-bay `/connect`)

lighthouse-bay’s **MindsDB adapter** should treat the Fly app as an HTTPS MindsDB HTTP API endpoint (not MySQL/Postgres wire protocol on Fly’s edge).

| Setting | Value |
|---------|--------|
| Base URL | `https://<app-name>.fly.dev` |
| Health | `GET /api/util/ping` |
| SQL (REST) | `POST /api/sql/query` with JSON body `{"query": "<SQL>"}` |
| Auth | HTTP basic / session per MindsDB when `MINDSDB_USERNAME` + `MINDSDB_PASSWORD` are set |

Example connect configuration (shape only — store credentials in lighthouse-bay secrets, not in repo):

```json
{
  "adapter": "mindsdb",
  "baseUrl": "https://mindsdb-lighthouse-bay.fly.dev",
  "username": "<from MINDSDB_USERNAME secret>",
  "password": "<from MINDSDB_PASSWORD secret>"
}
```

Example query from lighthouse-bay or a worker:

```bash
curl -fsS -u "$MINDSDB_USERNAME:$MINDSDB_PASSWORD" \
  -H 'Content-Type: application/json' \
  -d '{"query":"SHOW DATABASES;"}' \
  "https://mindsdb-lighthouse-bay.fly.dev/api/sql/query"
```

**Cold starts:** With scale-to-zero, the first request after idle may wait while Fly starts a machine. Retries with backoff in the adapter are sufficient; route wake traffic for *other* stack services through ontology-stack’s existing wake proxy, not a second proxy in this repo.

## Scale-to-zero behavior

`deploy/fly/fly.toml` sets:

- `auto_stop_machines = "stop"`
- `auto_start_machines = true`
- `min_machines_running = 0`

Fly Proxy stops idle machines after a few minutes of low traffic; there is no separate `scale_down_delay` knob in `fly.toml`. To keep one machine warm, set `min_machines_running = 1` (accepts higher cost).

## Operations

```bash
fly status --app mindsdb-lighthouse-bay
fly logs --app mindsdb-lighthouse-bay
fly ssh console --app mindsdb-lighthouse-bay
fly scale count 1 --app mindsdb-lighthouse-bay   # single machine recommended with one volume
```

## Local image smoke test (optional)

```bash
docker build -f docker/mindsdb.Dockerfile --target fly -t mindsdb-fly:local .
docker run --rm -p 47334:47334 -e MINDSDB_STORAGE_DIR=/tmp/mdb mindsdb-fly:local
curl -fsS http://127.0.0.1:47334/api/util/ping
```

## Files

| File | Role |
|------|------|
| `fly.toml` | Fly app config (region, autostop, checks, volume mount) |
| `mindsdb_config.fly.json` | Baked MindsDB config (HTTP on 47334, storage under `/data`) |
| `../docker/mindsdb.Dockerfile` (`fly` target) | Production container entrypoint |
