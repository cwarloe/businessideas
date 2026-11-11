/* Oats & More GitHub Pages -> standalone Cloudflare Worker voting adapter.
 * Does nothing while vote-config.js has an empty API origin.
 * When configured, intercepts the demo button to send real votes. */
(function () {
  'use strict';
  const origin = (window.OATS_VOTING_API || '').trim().replace(/\/+$/, '');
  if (!origin) return;
  const button = document.getElementById('vote-submit');
  const message = document.getElementById('vote-message');
  const options = Array.from(document.querySelectorAll('input[name="poll"]'));
  if (!button || !message || !options.length) return;
  const pollId = 'first-bowl';
  const key = 'oats-real-ballot-token-' + pollId;
  let token = '';
  try { token = localStorage.getItem(key) || ''; } catch {}
  const container = document.createElement('div');
  container.id = 'live-poll-results';
  container.setAttribute('aria-live', 'polite');
  container.style.marginTop = '18px';
  message.after(container);
  function showMessage(text) { message.textContent = text; }
  function headers() {
    return token ? { 'X-Ballot-Token': token } : {};
  }
  async function api(path, options = {}) {
    const res = await fetch(origin + path, { ...options, headers: { ...headers(), ...(options.headers || {}) } });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || 'The poll service is unavailable.');
    return data;
  }
  function render(data) {
    if (!data || !data.poll) return;
    const selected = data.my_choice;
    if (selected) {
      const input = options.find(x => x.value === selected);
      if (input) input.checked = true;
    }
    button.textContent = data.voted ? 'Update my vote' : 'Vote for this bowl';
    if (data.poll.status !== 'open') {
      button.disabled = true;
      button.textContent = 'Voting is closed';
    }
    container.replaceChildren();
    if (!data.results) {
      const p = document.createElement('p');
      p.textContent = data.results_hidden_reason || 'Vote to see the results.';
      container.appendChild(p);
      return;
    }
    const title = document.createElement('h3');
    title.textContent = 'Current community favorites';
    container.appendChild(title);
    const total = document.createElement('p');
    total.textContent = data.results.total_voters + ' recorded vote' + (data.results.total_voters === 1 ? '' : 's') + ' · You can change your choice.';
    container.appendChild(total);
    data.options.forEach(o => {
      const row = document.createElement('div');
      row.style.display = 'flex';
      row.style.justifyContent = 'space-between';
      row.style.gap = '1em';
      row.style.padding = '.35em 0';
      const name = document.createElement('span');
      name.textContent = o.label;
      const count = document.createElement('strong');
      count.textContent = String(o.votes || 0);
      row.append(name, count);
      container.append(row);
    });
  }
  button.textContent = 'Checking voting…';
  button.disabled = true;
  api('/api/polls/' + pollId).then(data => {
    render(data);
    if (data.poll.status === 'open') {
      button.disabled = false;
      showMessage('Votes are now collected and counted across visitors.');
    }
  }).catch(err => {
    button.textContent = 'Live voting unavailable';
    showMessage(err.message + ' Your choice has not been submitted.');
  });
  // Capture listener runs before the earlier local-only demo listener.
  button.addEventListener('click', async function (event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (button.disabled) return;
    const selected = options.find(x => x.checked);
    if (!selected) { showMessage('Choose a bowl first.'); return; }
    button.disabled = true;
    showMessage('Submitting your vote…');
    try {
      const data = await api('/api/polls/' + pollId + '/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice: selected.value })
      });
      if (data.ballot_token) {
        token = data.ballot_token;
        try { localStorage.setItem(key, token); } catch {
          showMessage('Vote recorded, but this browser cannot remember it for future edits.');
        }
      }
      render(data);
      showMessage('Thanks! Your vote has been counted.');
    } catch (err) {
      showMessage('Your vote was not confirmed: ' + err.message);
    } finally {
      button.disabled = false;
      if (button.textContent === 'Checking voting…') button.textContent = 'Vote for this bowl';
    }
  }, { capture: true });
})();