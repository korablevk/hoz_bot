#!/usr/bin/env bash

set -e

alembic revision -m "$1" --autogenerate
alembic upgrade head
exec poetry run python hozbot/main.py