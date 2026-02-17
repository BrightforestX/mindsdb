## Plan: Run MindsDB Locally via Python Module (with http,mysql,mcp,a2a)

This plan lets you run MindsDB from source using the Python module with your existing `mindsdb/config.json` and `MINDSDB_APIS=http,mysql,mcp,a2a`. It also keeps you Docker-ready by relying on environment variables that can be reused.

### 1) Prerequisites
- Python 3.9+
- Virtual environment available (`python3 -m venv`)
- Project path:
  - `/Users/clifforddalsoniii/Documents/Brightforest/projects/development/active/ml/mindsdb`

### 2) Create venv and install mindsdb from source
```bash
cd /Users/clifforddalsoniii/Documents/Brightforest/projects/development/active/ml/mindsdb
python3 -m venv mindsdb-venv
source mindsdb-venv/bin/activate
pip install -U pip
pip install -e .
```

### 3) Environment variables
Use a `.env` file (recommended) or export directly. These match your config and enable all APIs you selected (http,mysql,mcp,a2a).

```bash
# .env (example)
MINDSDB_USERNAME=new_username
MINDSDB_PASSWORD=new_password
MINDSDB_APIS=http,mysql,mcp,a2a
MINDSDB_LOG_LEVEL=DEBUG
MINDSDB_DEFAULT_PROJECT=mindsdb
MINDSDB_GUI_AUTOUPDATE=false
MINDSDB_NO_STUDIO=false
USE_PIDFILE=0

# Use your local config.json inside the repo
MINDSDB_CONFIG_PATH=/Users/clifforddalsoniii/Documents/Brightforest/projects/development/active/ml/mindsdb/mindsdb/config.json

# MindsDB configuration storage (Supabase). Prefer currentSchema for Postgres clients.
# NOTE: URL-encode any special characters in the password.
MINDSDB_DB_CON=postgresql://postgres.eawhngbgscalpjagxmvs:qpKep%26As%21MQRtX5jXy%21%21ibqN5S5@aws-1-us-east-1.pooler.supabase.com:5432/postgres?currentSchema=mindsdb_database_conn_str
```

Load env:
```bash
set -a; source .env; set +a
```

Reference: MindsDB environment variables https://docs.mindsdb.com/setup/environment-vars

### 4) Run MindsDB (Python module)
```bash
python -m mindsdb --config="$MINDSDB_CONFIG_PATH"
```

Apple Silicon (if architecture errors):
```bash
arch -arm64 python -m mindsdb --config="$MINDSDB_CONFIG_PATH"
```

### 5) Verify it’s running
```bash
# Status
curl -s http://127.0.0.1:47334/api/status | jq

# Login (auth enabled)
curl -s -i -c /tmp/mdb_cookies.txt -X POST http://127.0.0.1:47334/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"new_username","password":"new_password"}' | head -20

# Simple SQL check
curl -s http://127.0.0.1:47334/api/sql/query \
  -H 'Content-Type: application/json' \
  --data '{"query":"SELECT 1 AS ok"}' | jq
```

### 6) Stop
```bash
# If running in foreground: Ctrl + C
# If needed:
pkill -f "python -m mindsdb" || true
```

### 7) Troubleshooting
- Ports busy (47334/47335): kill lingering processes and retry.
- Login 405 vs /api/default/login: use `/api/login` for server v25.x (Studio bundles may differ).
- Passwords with special characters must be URL-encoded in `MINDSDB_DB_CON`.
- Schema not found in Supabase: ensure `mindsdb_database_conn_str` exists and user has privileges.

### 8) Optional: Switch to Docker later
- Reuse the same `.env` with `--env-file ./.env`.
- Mount a container config at `/etc/mindsdb/config.json` and set `MINDSDB_CONFIG_PATH=/etc/mindsdb/config.json`.

This keeps local and container runs consistent by relying on the same environment variables.


