#!/usr/bin/env bash
set -eu

base=https://sandboxlabs.ai/travel-stylist
failed=0
for asset in sponsored.js sponsored-ads.js; do
  url="$base/$asset"
  if ! metadata=$(curl --silent --show-error --output /dev/null --max-time 30 \
    --write-out '%{http_code} %{content_type}' "$url"); then
    failed=1
    continue
  fi
  status=${metadata%% *}
  mime=${metadata#* }
  mime=${mime%%;*}
  mime=$(printf '%s' "$mime" | tr '[:upper:]' '[:lower:]')
  if [[ "$status" != 200 ]]; then
    printf 'FAIL %s (HTTP %s)\n' "$url" "$status" >&2
    failed=1
    continue
  fi
  case "$mime" in
    application/javascript|text/javascript|application/ecmascript|text/ecmascript)
      printf 'PASS %s (%s)\n' "$asset" "$metadata" ;;
    *) printf 'FAIL %s (%s)\n' "$url" "$metadata" >&2; failed=1 ;;
  esac
done
exit "$failed"
