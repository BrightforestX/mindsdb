#!/usr/bin/env bash
set -euo pipefail

CONFIG="${HOME}/.mindsdb/config.json"
MINDSDB_DIR="/Users/clifforddalsoniii/Documents/Brightforest/projects/experiments/active/ml/mindsdb"
VENV="${MINDSDB_DIR}/mindsdb-venv"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found: $CONFIG" >&2
  exit 1
fi

if [ ! -d "$MINDSDB_DIR" ]; then
  echo "MindsDB dir not found: $MINDSDB_DIR" >&2
  exit 1
fi

echo "Stopping existing MindsDB..."
pkill -f "python .*mindsdb" || true
for p in 47334 47335; do
  pids=$(lsof -ti :$p || true)
  if [ -n "${pids}" ]; then
    kill -9 $pids || true
  fi
done

# Wait until ports are free (up to 10s)
for i in {1..10}; do
  if ! lsof -ti :47334 >/dev/null 2>&1 && ! lsof -ti :47335 >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

cd "$MINDSDB_DIR"

# If MySQL port still busy, bump to 47336 in config
MQ_PORT=47335
if lsof -ti :$MQ_PORT >/dev/null 2>&1; then
  NEW_PORT=47336
  python - <<'PYCONF'
import json, os
conf_path = os.path.expanduser("~/.mindsdb/config.json")
with open(conf_path) as f:
    data = json.load(f)
if isinstance(data.get("api"), dict) and isinstance(data["api"].get("mysql"), dict):
    data["api"]["mysql"]["port"] = 47336
    with open(conf_path, "w") as f:
        json.dump(data, f, indent=2)
print(f"Adjusted MySQL port to 47336 in {conf_path}")
PYCONF
fi

if [ -f "$VENV/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "$VENV/bin/activate"
fi

# Select Python interpreter
if [ -x "$VENV/bin/python" ]; then
  PYTHON="$VENV/bin/python"
else
  PYTHON="$(command -v python)"
fi

export MINDSDB_APIS=http,mysql,jobs,tasks,ml_task_queue,litellm
export MINDSDB_CONFIG_PATH="$CONFIG"

LOG_FILE="${HOME}/.mindsdb/mindsdb-run.log"
: > "$LOG_FILE"

echo "Starting MindsDB with config: $CONFIG"
"$PYTHON" -V
file "$PYTHON"
uname -m
"$PYTHON" -m mindsdb --config="$CONFIG" >>"$LOG_FILE" 2>&1 &
PID=$!
echo "MindsDB PID: $PID"

echo "Waiting for HTTP API on 127.0.0.1:47334 ..."
for i in {1..30}; do
  if curl -s http://127.0.0.1:47334/api/status >/dev/null; then
    echo "MindsDB is up at http://127.0.0.1:47334/"
    exit 0
  fi
  sleep 1
done

echo "MindsDB did not become ready in time. Check logs." >&2
exit 1
