#!/usr/bin/env bash
# Download the public reference documents listed in docs/research/manifests/public-docs.sha256
# into a caller-chosen directory (default: ./acq/law-docs, gitignored) and verify SHA-256.
# Usage: scripts/research/fetch-public-docs.sh [DEST_DIR]
set -euo pipefail
here="$(cd "$(dirname "$0")/../.." && pwd)"
manifest="$here/docs/research/manifests/public-docs.sha256"
dest="${1:-$here/acq/law-docs}"
mkdir -p "$dest"
status=0
while read -r sha name url; do
  [[ -z "$sha" || "$sha" == \#* ]] && continue
  out="$dest/$name"
  if [[ ! -f "$out" ]]; then
    echo "fetching $name"
    curl -fsSL -m 600 -A "Mozilla/5.0" -o "$out" "$url" || { echo "FETCH FAILED $name"; status=1; continue; }
  fi
  actual="$(sha256sum "$out" | cut -d' ' -f1)"
  if [[ "$actual" == "$sha" ]]; then echo "OK   $name"; else echo "MISMATCH $name expected $sha got $actual"; status=1; fi
done < "$manifest"
exit $status
