#!/usr/bin/env bash
set -eu

base=https://sandboxlabs.ai/travel-stylist
for asset in sponsored.js sponsored-ads.js; do
  url="$base/$asset"
  metadata=$(curl --silent --show-error --output /dev/null --max-time 30 \
    --write-out '%{http_code} %{content_type}' "$url")
  status=${metadata%% *}
  mime=${metadata#* }
  mime=${mime%%;*}
  mime=$(printf '%s' "$mime" | tr '[:upper:]' '[:lower:]')
  case "$status $mime" in
    '200 application/javascript'|'200 text/javascript'|'200 application/ecmascript'|'200 text/ecmascript')
      printf 'PASS %s (%s)\n' "$asset" "$metadata" ;;
    *) printf 'FAIL %s (%s)\n' "$url" "$metadata" >&2; exit 1 ;;
  esac
done
