#!/usr/bin/env bash
# Copies the shared fixture app into the run's empty workspace (the cwd).
# Runs only under `claude plugin eval --scaffold`.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/../fixture/app/." .
