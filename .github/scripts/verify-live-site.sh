#!/usr/bin/env bash
# Detect GitHub Pages deployments that lag behind the repository's main branch.
set -euo pipefail

build_id="${GITHUB_SHA:-$(git rev-parse HEAD)}"
site="https://cwarloe.github.io/businessideas/oats-and-more"
sources=("docs/oats-and-more/index.html" "docs/oats-and-more/release.js")
urls=("$site/index.html" "$site/release.js")
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
    echo "Published Oats site matches source commit ${build_id:0:8}."
    exit 0
  fi
  if ((attempt < attempts)); then sleep 15; fi
done

echo "ERROR: Published Oats site did not match $build_id after $attempts attempts." >&2
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  echo "### Deployment mismatch: Oats, Etc." >> "$GITHUB_STEP_SUMMARY"
  echo "The live homepage or release script did not match commit \`$build_id\` after retries. Check the GitHub Pages deployment and CDN." >> "$GITHUB_STEP_SUMMARY"
fi
exit 1
