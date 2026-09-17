#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt
python -m eval.run_eval
python -c "from app.orchestrator import Orchestrator; Orchestrator().run_all()"
uvicorn app.main:app --host 0.0.0.0 --port 8000
