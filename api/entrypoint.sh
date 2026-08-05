#!/bin/sh
set -e

echo "Server is starting!"
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
