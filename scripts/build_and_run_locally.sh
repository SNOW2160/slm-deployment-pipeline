#!/usr/bin/env bash
set -e

docker build -t slm-starter:local .
docker run --rm -p 8000:8000 -e API_KEY=devkey slm-starter:local
