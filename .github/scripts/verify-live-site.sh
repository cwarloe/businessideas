#!/usr/bin/env bash
# Detect GitHub Pages deployments that lag behind the repository's main branch.
set -euo pipefail

build_id="${GITHUB_SHA:-$(git rev-parse HEAD)}"
site="https://cwarloe.github.io/businessideas/oats-and-more"
portfolio_site="https://cwarloe.github.io/businessideas"
sources=(
  "docs/oats-and-more/index.html"
  "docs/oats-and-more/design-lab.html"
  "docs/oats-and-more/research.html"
  "docs/oats-and-more/menu-board.html"
  "docs/oats-and-more/vote-admin.html"
  "docs/oats-and-more/design-assets.js"
  "docs/oats-and-more/vote-config.js"
  "docs/oats-and-more/vote-live.js"
  "docs/oats-and-more/release.js"
  "docs/decision-history.html"
  "docs/data/decision-history.json"
)
urls=(
  "$site/index.html"
  "$site/design-lab.html"
  "$site/research.html"
  "$site/menu-board.html"
  "$site/vote-admin.html"
  "$site/design-assets.js"
  "$site/vote-config.js"
  "$site/vote-live.js"
  "$site/release.js"
  "$portfolio_site/decision-history.html"
  "$portfolio_site/data/decision-history.json"
)
attempts=24

for ((attempt = 1; attempt <= attempts; attempt++)); do
  matched=true
  for i in "${!sources[@]}"; do
    source="${sources[$i]}"
    url="${urls[$i]}"
    expected="$(sha256sum "$source" | cut -d' ' -f1)"
    if actual="$(curl --fail --silent --show-error --location \
      --connect-timeout 10 --max-time 30 --retry 2 --retry-delay 2 \
      -H 'Cache-Control: no-cache' "$url?verify=$build_id" | sha256sum | cut -d' ' -f1)"; then
      if [[ "$actual" == "$expected" ]]; then
        echo "PASS: $url matches ${source} (${expected:0:8})"
        continue
      fi
      echo "WAIT ($attempt/$attempts): $url is ${actual:0:8}; expected ${expected:0:8}"
    else
      echo "WAIT ($attempt/$attempts): could not retrieve $url"
    fi
    matched=false
  done

  if [[ "$matched" == true ]]; then
    echo "Published Business Ideas assets match source commit ${build_id:0:8}."
    exit 0
  fi
  if ((attempt < attempts)); then sleep 15; fi
done

echo "ERROR: Published Business Ideas assets did not match $build_id after $attempts attempts." >&2
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  echo "### Deployment mismatch: Business Ideas" >> "$GITHUB_STEP_SUMMARY"
  echo "A live page or asset did not match commit \`$build_id\` after retries. Check the GitHub Pages deployment and CDN." >> "$GITHUB_STEP_SUMMARY"
fi
exit 1
