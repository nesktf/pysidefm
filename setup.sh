#!/usr/bin/env bash

if [[ -d venv/ ]]; then
  echo "Deleting old venv..."
  rm -rf venv/
fi

mkdir -p venv/
python3 -m venv venv/

echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Done!"
