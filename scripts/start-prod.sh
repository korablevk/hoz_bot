#!/usr/bin/env bash

set -e

export DEBUG=False
exec poetry run python hozbot/bot.py