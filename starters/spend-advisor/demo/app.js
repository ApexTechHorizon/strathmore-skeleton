/* Same-origin operator demo; never store the service key or render API HTML. */
const form = document.getElementById('request');
const controls = document.getElementById('controls');
const status = document.getElementById('status');
const items = document.getElementById('items');
const metrics = document.getElementById('metrics');
let busy = false;

async function post(path, body, key) {
  const response = await fetch(path, {
    method: 'POST', headers: {'Content-Type': 'application/json', Authorization: `Bearer ${key}`},
    body: JSON.stringify(body), cache: 'no-store',
  });
  if (!response.ok) {
    const messages = {401: 'Invalid service key.', 404: 'No matching snapshot or delivered offer.',
      409: 'Offer changed. Get suggestions again before deciding.', 422: 'Check the household, month and year.',
      503: 'Feedback storage unavailable. Try again later.'};
    throw new Error(messages[response.status] || `Request failed (${response.status}).`);
  }
  return response.json();
}

async function run(action) {
  if (busy) return;
  busy = true;
  controls.disabled = true;
  for (const button of items.querySelectorAll('button')) button.disabled = true;
  status.textContent = 'Working…';
  try {
    await action();
    status.textContent = 'Updated. These are synthetic planning examples.';
  } catch (error) {
    status.textContent = error.message;
    if (metrics.textContent === 'Loading…') metrics.textContent = 'No metrics available for this request.';
  } finally {
    busy = false;
    controls.disabled = false;
    for (const button of items.querySelectorAll('button')) button.disabled = false;
  }
}

function render(offers, period, key) {
  items.replaceChildren();
  if (!offers.length) {
    items.textContent = 'No justified reduction suggestions for this period.';
    return;
  }
  for (const offer of offers) {
    const article = document.createElement('article');
    const title = document.createElement('h2');
    title.textContent = `Potential reduction: KES ${Number(offer.item.savingKes).toFixed(2)}`;
    const reason = document.createElement('p');
    reason.textContent = offer.item.reason;
    article.append(title, reason);
    for (const [action, label] of [['accepted', 'Accept suggestion'], ['declined', 'Decline suggestion']]) {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.addEventListener('click', () => run(async () => {
        await post('/recommendations/feedback', {...period, offerId: offer.offerId,
          expectedRevision: offer.revision, action}, key);
        // Fetch the current revision instead of replaying a decision against stale state.
        const next = await post('/recommendations/offers', period, key);
        render(next.offers, period, key);
        metrics.textContent = JSON.stringify(await post('/recommendations/metrics', period, key), null, 2);
      }));
      article.append(button);
    }
    items.append(article);
  }
}

form.addEventListener('submit', event => {
  event.preventDefault();
  const period = {userId: document.getElementById('household').value,
    month: Number(document.getElementById('month').value), year: Number(document.getElementById('year').value)};
  const key = document.getElementById('key').value;
  run(async () => {
    items.replaceChildren();
    metrics.textContent = 'Loading…';
    const result = await post('/recommendations/offers', period, key);
    render(result.offers, period, key);
    // The cards are now displayed. Delivery alone is not counted as display.
    for (const offer of result.offers) {
      await post('/recommendations/feedback', {...period, offerId: offer.offerId,
        expectedRevision: offer.revision, action: 'shown'}, key);
    }
    metrics.textContent = JSON.stringify(await post('/recommendations/metrics', period, key), null, 2);
  });
});
