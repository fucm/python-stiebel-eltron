#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync 