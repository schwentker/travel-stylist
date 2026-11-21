// Read-only UCP Ask probe for one stock jacket on Aesido's storefront. Node 22+.
import { createHash, createPrivateKey, createPublicKey, randomUUID, sign } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const store = 'https://www.aesido.com';
const productPath = '/products/mens-vintage-two-button-notch-lapel-blazer';
const version = '2026-08-25';
const capability = 'dev.ucp.common.ask';

async function readJson(url, options = {}) {
  const response = await fetch(url, { ...options, redirect: 'error', signal: AbortSignal.timeout(30000) });
  const text = await response.text();
  if (!response.ok) {
    throw new Error(`${url.hostname || new URL(url).hostname} HTTP ${response.status}: ${text.slice(0, 400)}`);
  }
  if (response.headers.get('content-type')?.includes('text/event-stream')) {
    for (const event of text.split(/\r?\n\r?\n/)) {
      const data = event.split(/\r?\n/).filter(line => line.startsWith('data:'));
      if (!data.length) continue;
      const message = JSON.parse(data.map(line => line.slice(5).trimStart()).join('\n'));
      if (message.id === 1) return message;
    }
    throw new Error('Missing JSON-RPC reply in merchant event stream.');
  }
  return JSON.parse(text);
}

function signedHeaders(endpoint, profile, body, privateKey, kid) {
  const digest = createHash('sha256').update(body).digest('base64');
  const headers = {
    'content-type': 'application/json',
    'content-digest': `sha-256=:${digest}:`,
    'ucp-agent': `profile="${profile}"`,
    'idempotency-key': randomUUID(),
  };
  const covered = { '@method': 'POST', '@authority': endpoint.host, '@path': endpoint.pathname, ...headers };
  const components = Object.keys(covered).map(name => `"${name}"`).join(' ');
  const params = `(${components});created=${Math.floor(Date.now() / 1000)};keyid="${kid}";alg="ecdsa-p256-sha256"`;
  const lines = Object.entries(covered).map(([name, value]) => `"${name}": ${value}`);
  lines.push(`"@signature-params": ${params}`);
  const signature = sign('sha256', Buffer.from(lines.join('\n')), { key: privateKey, dsaEncoding: 'ieee-p1363' });
  return { ...headers, accept: 'application/json, text/event-stream',
    'signature-input': 'sig1=' + params, signature: `sig1=:${signature.toString('base64')}:` };
}

async function probe() {
  const input = process.argv[2];
  if (!input) throw new Error('Pass the public HTTPS URL of your ucp.json as the first argument.');
  const profile = new URL(input);
  if (profile.protocol !== 'https:' || profile.username || profile.password || profile.hash) {
    throw new Error('Use a public HTTPS profile URL without credentials or a fragment.');
  }
  const keyPath = process.env.UCP_SIGNING_KEY_PATH || join(homedir(), '.config/travel-stylist/ucp-signing.pem');
  const privateKey = createPrivateKey(readFileSync(keyPath));
  const publicKey = createPublicKey(privateKey).export({ format: 'jwk' });
  const identity = await readJson(profile);
  const key = identity.keys?.find(k => k.crv === 'P-256' && k.kty === 'EC' &&
    k.x === publicKey.x && k.y === publicKey.y && !('d' in k));
  if (!key || !/^[A-Za-z0-9._-]+$/.test(key.kid) || !identity.ucp?.capabilities?.[capability]?.some(c => c.version === version)) {
    throw new Error('The hosted Ask profile must contain the public P-256 key matching the local PEM and a valid key ID.');
  }

  const poppy = await readJson(store + '/.well-known/poppy.json');
  const discovery = poppy.agent?.protocols?.find(p => p.type === 'ucp')?.endpoint;
  if (discovery !== store + '/.well-known/ucp') throw new Error('Aesido UCP discovery changed.');
  const { ucp } = await readJson(discovery);
  const service = ucp.services?.['dev.ucp.common']?.find(s => s.transport === 'mcp' && s.version === version);
  if (!ucp.capabilities?.[capability]?.some(c => c.version === version) ||
      service?.endpoint !== 'https://aesido.myshopify.com/api/ucp/mcp') {
    throw new Error('Aesido no longer advertises the expected Shopify Ask endpoint.');
  }
  const endpoint = new URL(service.endpoint);
  const product = await readJson(store + productPath + '.js');
  const variant = product.variants?.find(v => v.id === 41550385872942 && v.options?.includes('40R'));
  if (variant?.available !== true) throw new Error('The exact Aesido 40R variant is unavailable.');
  const variantId = 'gid://shopify/ProductVariant/' + variant.id;
  const question = 'Can a US buyer return one standard stock ' + product.title + ' (' + variant.title +
    ') for a refund? Do custom-order, single-item or final-sale exclusions apply? Identify the official terms.';
  const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'ask_business',
    arguments: { meta: { 'ucp-agent': { profile: profile.href } },
      ask: { query: question, ids: [variantId], context: { address_country: 'US', language: 'en' } } } } });
  const response = await readJson(endpoint, { method: 'POST', body,
    headers: signedHeaders(endpoint, profile.href, body, privateKey, key.kid) });
  if (response.id !== 1 || response.error || response.result?.isError) {
    throw new Error('Merchant RPC error: ' + JSON.stringify(response.error ?? response.result?.content ?? 'Missing or mismatched RPC result').slice(0, 400));
  }
  const result = response.result;
  const reply = result.structuredContent || JSON.parse(result.content[0].text);
  if (reply.ucp?.status === 'error' || typeof reply.answer?.plain !== 'string' || !reply.answer.plain.trim()) {
    throw new Error('No merchant answer returned for this request.');
  }
  console.log(JSON.stringify({ seller: 'Aesido', variantId, question, observedAt: new Date().toISOString(),
    indicativeSellerReply: reply.answer.plain }, null, 2));
}

probe().catch(error => { console.error(error.message); process.exitCode = 1; });
