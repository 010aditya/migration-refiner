#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo '✅ Environment ready. Run with: python main.py'
