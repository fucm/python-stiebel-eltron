#!/usr/bin/env bash

uv run scripts/generate.py
uvx ruff format src
