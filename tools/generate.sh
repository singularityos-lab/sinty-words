#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
for lang in en it de fr es pt_BR; do
  src=$(echo "$lang" | tr 'A-Z' 'a-z')
  curl -sfL "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/mono/$src.txt.gz" \
    | gzip -dc 2>/dev/null | python3 -I tools/count.py "$lang" 8000000 "$work/$lang.counts" || true
  python3 -I tools/build.py "$(echo "$lang" | cut -c1-2)" "$work/$lang.counts" "data/$lang.words"
done
