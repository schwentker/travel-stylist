#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
docker info >/dev/null
umask 077
scratch_dir=$(mktemp -d)
trap 'rm -f "$scratch_dir/providers.json"; rmdir "$scratch_dir"' EXIT
node --env-file-if-exists=.env --input-type=module - "$scratch_dir/providers.json" <<'JS'
import { writeFileSync } from 'node:fs';
const names = ['SENSO_API_KEY', 'TYPESAFE_API_KEY', 'JEV_API_KEY', 'SHOPIFY_CATALOG_TOKEN'];
const values = Object.fromEntries(names.filter(k => process.env[k]).map(k => [k, process.env[k]]));
writeFileSync(process.argv[2], JSON.stringify(values));
JS
npx --yes wrangler@4.166.0 deploy --config commerce/wrangler.jsonc --secrets-file "$scratch_dir/providers.json"
