#!/bin/bash
# Build pipeline: generate HTML (zero-dep) then compile a minimal production
# Tailwind CSS by scanning the generated HTML (captures all used + dynamic classes).
set -e
cd "$(dirname "$0")"
python3 build.py
TW="${TAILWIND_BIN:-$HOME/.local/bin/tailwindcss}"
"$TW" -i input.css -o site/styles.css --minify
echo "styles.css: $(stat -c%s site/styles.css) bytes"
