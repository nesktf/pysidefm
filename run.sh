#!/usr/bin/env bash

if [[ ! -d venv/ ]]; then
  echo "venv not setup, run setup.sh"
  exit 1
fi

source venv/bin/activate
python3 __main__.py
