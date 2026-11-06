const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Element {
  constructor(tag = '') {
    this.tag = tag;
    this.children = [];
    this.events = {};
    this.value = '';
    this.textContent = '';
    this.disabled = false;
  }
  append(...children) { this.children.push(...children); }
  replaceChildren() { this.children = []; this.textContent = ''; }
  addEventListener(name, handler) { this.events[name] = handler; }
  querySelectorAll(tag) {
    return this.children.flatMap(child => [
      ...(child.tag === tag ? [child] : []), ...child.querySelectorAll(tag),
    ]);
  }
}

function page(handler) {
  const nodes = Object.fromEntries(['request', 'controls', 'status', 'items', 'metrics',
    'key', 'household', 'month', 'year'].map(id => [id, new Element()]));
  Object.assign(nodes.key, {value: 'private-demo-key'});
  Object.assign(nodes.household, {value: 'demo-household'});
  nodes.month.value = '6';
  nodes.year.value = '2026';
  const calls = [];
  const context = vm.createContext({document: {
    getElementById: id => nodes[id], createElement: tag => new Element(tag),
  }, fetch: async (route, options) => {
    const body = JSON.parse(options.body);
    calls.push({route, body, headers: options.headers});
    return handler(route, body);
  }});
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../demo/app.js'), 'utf8'), context);
  return {nodes, calls, submit: () => nodes.request.events.submit({preventDefault() {}})};
}

const ok = value => ({ok: true, json: async () => value});
const offer = {offerId: 'a'.repeat(64), revision: 0, item: {
  savingKes: 400, reason: '<img src=x onerror=alert(1)> synthetic reason',
}};
const tick = () => new Promise(resolve => setImmediate(resolve));

test('renders text safely, acknowledges display, and refreshes revision after a decision', async () => {
  let revision = 0;
  const p = page((route, body) => {
    if (route.endsWith('/offers')) return ok({offers: [{...offer, revision}]});
    if (route.endsWith('/feedback') && body.action !== 'shown') revision++;
    return ok({accepted: revision, acceptRate: revision ? 1 : 0});
  });
  p.submit();
  await tick();
  assert.equal(p.nodes.items.children.length, 1);
  const article = p.nodes.items.children[0];
  assert.equal(article.children[1].textContent, offer.item.reason);
  assert.match(article.children[0].textContent, /KES 400\.00/);
  assert.equal(p.calls[1].body.action, 'shown');
  await article.children[2].events.click();
  assert.equal(p.calls.find(c => c.body.action === 'accepted').body.expectedRevision, 0);
  const newArticle = p.nodes.items.children[0];
  await newArticle.children[3].events.click();
  assert.equal(p.calls.find(c => c.body.action === 'declined').body.expectedRevision, 1);
  assert.equal(p.nodes.controls.disabled, false);
});

test('blocks duplicate submits and captures the correct household/key for each request', async () => {
  let release;
  const waiting = new Promise(resolve => { release = resolve; });
  const p = page(async () => { await waiting; return ok({offers: []}); });
  p.submit();
  p.submit();
  assert.equal(p.calls.length, 1);
  assert.equal(p.nodes.controls.disabled, true);
  p.nodes.household.value = 'changed-during-request';
  release();
  await tick();
  assert.equal(p.calls[0].body.userId, 'demo-household');
  assert.equal(p.calls[0].headers.Authorization, 'Bearer private-demo-key');
  assert.match(p.nodes.items.textContent, /No justified/);
});

test('unauthorized, conflict, and network failures restore controls without stale cards', async () => {
  for (const code of [401, 409, 503, 'offline']) {
    const p = page(() => {
      if (code === 'offline') throw new Error('Network unavailable');
      return {ok: false, status: code};
    });
    p.submit();
    await tick();
    assert.equal(p.nodes.controls.disabled, false);
    assert.equal(p.nodes.items.children.length, 0);
    assert.notEqual(p.nodes.status.textContent, 'Working…');
    assert.doesNotMatch(p.nodes.status.textContent, /Updated/);
    assert.equal(p.nodes.metrics.textContent, 'No metrics available for this request.');
  }
});
