#!/bin/sh
poetry run python -m uvicorn backend.main:app --reload --host=0.0.0.0 --port=8080