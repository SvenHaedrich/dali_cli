#!/bin/bash
export PYTHONPATH=../dali
[ -f venv/bin/activate ] || python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pytest cli/ "$@"
