#!/bin/sh
set -e

echo "AI service is starting!"
exec uvicorn src.main:app --host 0.0.0.0 --port 8100 --reload