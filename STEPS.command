#!/bin/sh
# Standalone macOS Finder / Dock launcher for STEPS outside DAW software.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
exec python3 -B -m app.start "$@"
