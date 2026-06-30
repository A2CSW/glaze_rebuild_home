#!/bin/bash
export PYTHONPATH=.
exec python -m streamlit run app/main.py "$@"
