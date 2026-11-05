#!/usr/bin/env bash
set -e
echo "AutoPilot Drift — serving on http://localhost:8080"
echo "Press Ctrl+C to stop."
python3 -m http.server 8080
