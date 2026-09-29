const form = document.querySelector('#recommendation-form');
const playedPlatform = document.querySelector('#played-platform');
const selectedPlatform = document.querySelector('#selected-platform');
const genre = document.querySelector('#genre');
const publisher = document.querySelector('#publisher');
const releaseDecade = document.querySelector('#release-decade');
const publisherOptions = document.querySelector('#publisher-options');
const results = document.querySelector('#results');
const resultCount = document.querySelector('#result-count');
const resultTitle = document.querySelector('#results-title');
const status = document.querySelector('#form-status');

function fillSelect(select, values, emptyLabel) {
  select.replaceChildren();
  if (emptyLabel) {
    select.add(new Option(emptyLabel, ''));
  }
  values.forEach((value) => select.add(new Option(value, value)));
}

async function loadOptions() {
  const response = await fetch('/api/options');
  if (!response.ok) throw new Error('Could not load catalog options.');
  const options = await response.json();
  fillSelect(playedPlatform, options.platforms, 'Select platform');
  fillSelect(selectedPlatform, options.platforms, 'Use played platform');
  fillSelect(genre, options.genres, 'Any genre');
  fillSelect(releaseDecade, options.decades, 'Any decade');
  publisherOptions.replaceChildren();
  options.publishers.forEach((value) => {
    publisherOptions.append(new Option(value, value));
  });
}

function formatIndianSales(millions) {
  const value = Number(millions);
  if (!Number.isFinite(value)) return '';
  const lakhs = value * 10;
  if (lakhs >= 100) return `${(lakhs / 100).toFixed(2)} crore predicted sales`;
  return `${lakhs.toFixed(lakhs >= 10 ? 1 : 2)} lakh predicted sales`;
}

function renderResults(payload) {
  const items = payload.results || [];
  const showScores = Boolean(payload.played_game && payload.played_platform);
  resultTitle.textContent = payload.played_game
    ? `Recommendations for ${payload.played_game}`
    : 'Top games for your filters';
  resultCount.textContent = `${items.length} result${items.length === 1 ? '' : 's'}`;
  results.replaceChildren();

  if (!items.length) {
    results.innerHTML = '<p class="empty-state">No games matched those settings.</p>';
    return;
  }

  items.forEach((item, index) => {
    const article = document.createElement('article');
    article.className = 'result';
    const year = item.Year ?? 'Unknown year';
    const score = showScores
      ? `<div class="score"><strong>${Number(item.Similarity_Score).toFixed(0)}%</strong>match score<span>${formatIndianSales(item.Predicted_Global_Sales)}</span></div>`
      : '';
    article.innerHTML = `
      <div class="rank">${index + 1}</div>
      <div>
        <h3>${item.Name}</h3>
        <p class="meta">${item.Platform} | ${item.Genre} | ${item.Publisher} | ${year}</p>
      </div>
      ${score}
    `;
    results.append(article);
  });
}

document.querySelectorAll('input[name="platform-mode"]').forEach((input) => {
  input.addEventListener('change', () => {
    selectedPlatform.disabled = input.value !== 'same' || !input.checked;
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  status.textContent = 'Finding recommendations...';
  resultCount.textContent = '';

  const mode = document.querySelector('input[name="platform-mode"]:checked').value;
  const playedGame = document.querySelector('#played-game').value.trim();
  const selectedGenre = genre.value || null;
  const selectedPublisher = publisher.value.trim() || null;
  const selectedDecade = releaseDecade.value || null;
  if (!playedGame && !selectedGenre && !selectedPublisher && !selectedDecade) {
    status.textContent = 'Enter a game or choose at least one filter.';
    return;
  }
  const payload = {
    played_game: playedGame || null,
    played_platform: playedPlatform.value || null,
    platform_mode: mode,
    selected_platform: mode === 'same' ? (selectedPlatform.value || null) : null,
    genre: selectedGenre,
    publisher: selectedPublisher,
    release_decade: selectedDecade,
    limit: Number(document.querySelector('#limit').value),
  };

  try {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || 'Recommendation request failed.');
    renderResults(body);
    status.textContent = '';
  } catch (error) {
    status.textContent = error.message;
    results.innerHTML = '<p class="empty-state">Check the game title and platform, then try again.</p>';
  }
});

loadOptions().catch((error) => { status.textContent = error.message; });
