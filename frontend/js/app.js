/**
 * TrailGemma Main App — clean, no globals pollution
 */
let currentTrails = [];
let selectedTrail = null;
let leafletMap    = null;
let markers       = [];
let grassSecs     = 0;

// ─── Boot ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  initSW();
  initGrassTimer();
  initTabs();
  initSunlightMode();
  initPocketMode();
  initChat();
  await getStatus();
  await loadTrails();
  await loadPresets();
});

// ─── Service Worker ─────────────────────────────────────────
function initSW() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }
}

// ─── Grass Timer ────────────────────────────────────────────
function initGrassTimer() {
  setInterval(() => {
    grassSecs++;
    const m = Math.floor(grassSecs / 60);
    const s = grassSecs % 60;
    const t = `${m}m ${String(s).padStart(2,'0')}s`;
    const el1 = document.getElementById('grass-counter');
    const el2 = document.getElementById('pocket-timer');
    if (el1) el1.textContent = t;
    if (el2) el2.textContent = t;
  }, 1000);
}

// ─── Tabs ────────────────────────────────────────────────────
function initTabs() {
  const pills = document.querySelectorAll('.nav-pill[data-tab]');
  const panes = document.querySelectorAll('.tab-pane');

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const target = pill.dataset.tab;
      pills.forEach(p => { p.classList.remove('active'); p.setAttribute('aria-selected', 'false'); });
      panes.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      pill.setAttribute('aria-selected', 'true');
      document.getElementById(target)?.classList.add('active');
      if (target === 'tab-foliage' && leafletMap) setTimeout(() => leafletMap.invalidateSize(), 120);
    });
  });
}

// ─── Sunlight Mode ───────────────────────────────────────────
function initSunlightMode() {
  const btn = document.getElementById('btn-sunlight');
  if (!btn) return;
  const saved = localStorage.getItem('tg-sunlight');
  if (saved === '1') document.body.classList.add('sunlight');
  btn.addEventListener('click', () => {
    document.body.classList.toggle('sunlight');
    localStorage.setItem('tg-sunlight', document.body.classList.contains('sunlight') ? '1' : '0');
  });
}

// ─── Pocket Mode ─────────────────────────────────────────────
function initPocketMode() {
  document.getElementById('pocket-overlay')?.addEventListener('click', () => {
    document.getElementById('pocket-overlay').classList.remove('active');
  });
}

function enterPocketMode() {
  document.getElementById('pocket-overlay')?.classList.add('active');
}
window.enterPocketMode = enterPocketMode;

// ─── System Status ───────────────────────────────────────────
async function getStatus() {
  try {
    const d = await (await fetch('/api/status')).json();
    const el = document.getElementById('status-model');
    if (el && d.gemma?.active_model) {
      el.textContent = d.gemma.active_model.replace('gemma2:2b', 'Gemma 2 · Local');
    }
  } catch {}
}

// ─── Trails ──────────────────────────────────────────────────
async function loadTrails() {
  try {
    currentTrails = await (await fetch('/api/trails')).json();
    renderTrailList();
    initMap();
    if (currentTrails.length) selectTrail(currentTrails[0].id);
  } catch (e) { console.error('Trails:', e); }
}

function renderTrailList() {
  const el = document.getElementById('trails-list-container');
  if (!el) return;
  el.innerHTML = currentTrails.map(t => `
    <div class="trail-item ${selectedTrail?.id === t.id ? 'active' : ''}"
         onclick="selectTrail('${t.id}')" tabindex="0" role="button"
         aria-pressed="${selectedTrail?.id === t.id}">
      <div class="trail-item-name">${t.name}</div>
      <div class="trail-item-desc">${t.description}</div>
      <div class="trail-stats">
        <span class="trail-stat">${t.distance_km} km</span>
        <span class="trail-stat">+${t.elevation_gain_m} m</span>
        <span class="trail-stat">${t.difficulty}</span>
        <span class="trail-stat">${t.canopy_composition.sugar_maple}% maple</span>
      </div>
    </div>
  `).join('');
}

function initMap() {
  const mapEl = document.getElementById('trail-map');
  if (!mapEl || typeof L === 'undefined') return;
  if (leafletMap) return;

  leafletMap = L.map('trail-map', { center: [44.275, -73.985], zoom: 10, zoomControl: true });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    maxZoom: 18
  }).addTo(leafletMap);

  currentTrails.forEach(t => {
    const m = L.circleMarker([t.lat, t.lng], {
      radius: 8, fillColor: '#22c55e', color: '#fff',
      weight: 2, opacity: 1, fillOpacity: 0.85
    }).addTo(leafletMap);
    m.bindPopup(`<strong style="color:#000">${t.name}</strong><br><small>${t.difficulty} · ${t.distance_km} km</small>`);
    m.on('click', () => selectTrail(t.id));
    markers.push(m);
  });
}

async function selectTrail(id) {
  selectedTrail = currentTrails.find(t => t.id === id);
  if (!selectedTrail) return;
  renderTrailList();

  const titleEl = document.getElementById('hero-trail-name');
  if (titleEl) titleEl.textContent = selectedTrail.name;

  if (leafletMap) leafletMap.flyTo([selectedTrail.lat, selectedTrail.lng], 13, { duration: 0.7 });

  await Promise.all([fetchFoliage(), fetchBirds()]);
}
window.selectTrail = selectTrail;

// ─── TabPFN — Foliage ────────────────────────────────────────
async function fetchFoliage() {
  if (!selectedTrail) return;
  try {
    const res = await fetch('/api/predict/foliage', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        elevation_m: selectedTrail.avg_elevation_m,
        latitude: selectedTrail.lat,
        sugar_maple_pct: selectedTrail.canopy_composition.sugar_maple,
        red_oak_pct: selectedTrail.canopy_composition.red_oak,
        aspen_birch_pct: selectedTrail.canopy_composition.aspen_birch,
        chilling_hours: selectedTrail.chilling_hours_est,
        day_of_year: 282
      })
    });
    TabPFNUI.renderFoliagePrediction('tabpfn-foliage-results', await res.json());
  } catch {}
}

// ─── TabPFN — Birds ──────────────────────────────────────────
async function fetchBirds() {
  if (!selectedTrail) return;
  try {
    const near = selectedTrail.id.includes('river') || selectedTrail.id.includes('cascade') ? 1 : 0;
    const res = await fetch('/api/predict/birds', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hour_of_day: 8.0, canopy_density_pct: 70.0,
        elevation_m: selectedTrail.avg_elevation_m,
        ambient_temp_c: 9.0, near_water: near
      })
    });
    TabPFNUI.renderBirdPrediction('tabpfn-bird-results', await res.json());
  } catch {}
}

// ─── Audio Briefing ──────────────────────────────────────────
async function triggerAudioBriefing() {
  if (!selectedTrail) return;
  const btn = document.getElementById('btn-generate-briefing');
  if (!btn) return;

  btn.classList.add('loading');
  btn.disabled = true;
  const orig = btn.innerHTML;
  btn.innerHTML = 'Synthesizing…';

  try {
    const res = await fetch('/api/briefing/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ trail_id: selectedTrail.id, hour_of_day: 8.5, day_of_year: 282 })
    });
    const data = await res.json();
    window.audioTour.load(data);
    document.getElementById('audio-player-card')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch {
    alert('Could not reach the backend. Make sure the server is running on :8000.');
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
    btn.innerHTML = orig;
  }
}
window.triggerAudioBriefing = triggerAudioBriefing;

// ─── Garden / Frost ──────────────────────────────────────────
async function loadPresets() {
  try {
    const presets = await (await fetch('/api/garden-presets')).json();
    const sel = document.getElementById('garden-preset-select');
    if (!sel) return;
    sel.innerHTML = presets.map((p, i) => `<option value="${i}">${p.name}</option>`).join('');
    sel.addEventListener('change', () => {
      const p = presets[sel.value];
      if (!p) return;
      setVal('frost-elev',       p.elevation_m);
      setVal('frost-dist-water', p.dist_water_km);
      setVal('frost-aspect',     p.slope_aspect_deg);
      setVal('frost-temp',       p.avg_night_temp_c);
      setVal('frost-moisture',   p.soil_moisture_pct);
      calculateTabPFNFrost();
    });
    calculateTabPFNFrost();
  } catch {}
}

function setVal(id, v) { const el = document.getElementById(id); if (el) el.value = v; }
function getVal(id, def) { const el = document.getElementById(id); return el ? parseFloat(el.value) : def; }

async function calculateTabPFNFrost() {
  try {
    const body = {
      elevation_m: getVal('frost-elev', 260),
      dist_water_km: getVal('frost-dist-water', 3.8),
      slope_aspect_deg: getVal('frost-aspect', 175),
      canopy_cover_pct: getVal('frost-canopy', 20),
      avg_night_temp_c: getVal('frost-temp', 3.2),
      soil_moisture_pct: getVal('frost-moisture', 38),
      day_of_autumn: 38
    };
    const res = await fetch('/api/predict/frost', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    TabPFNUI.renderFrostPrediction('tabpfn-frost-results', await res.json());
  } catch {}
}
window.calculateTabPFNFrost = calculateTabPFNFrost;

// ─── Gemma Chat ──────────────────────────────────────────────
function initChat() {
  const form  = document.getElementById('chat-form');
  const input = document.getElementById('chat-input');
  const hist  = document.getElementById('chat-history');
  if (!form || !input || !hist) return;

  const send = async () => {
    const q = input.value.trim();
    if (!q) return;
    appendMsg(hist, q, 'user');
    input.value = '';
    const thinking = appendMsg(hist, '…', 'ai');
    try {
      const res = await fetch('/api/naturalist/ask', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, trail_id: selectedTrail?.id, context: '' })
      });
      const d = await res.json();
      thinking.querySelector('.msg-body').textContent = d.answer;
    } catch {
      thinking.querySelector('.msg-body').textContent = 'Could not reach Gemma 2. Ensure Ollama is running locally.';
    }
    hist.scrollTop = hist.scrollHeight;
  };

  form.addEventListener('submit', e => { e.preventDefault(); send(); });
}

function appendMsg(hist, text, role) {
  const el = document.createElement('div');
  el.className = `msg msg-${role === 'user' ? 'user' : 'ai'}`;
  if (role === 'ai') {
    el.innerHTML = `<div class="msg-sender">Gemma Ranger</div><div class="msg-body">${text}</div>`;
  } else {
    el.textContent = text;
  }
  hist.appendChild(el);
  hist.scrollTop = hist.scrollHeight;
  return el;
}

function askQuestion(q) {
  const input = document.getElementById('chat-input');
  if (input) {
    input.value = q;
    document.getElementById('chat-form')?.dispatchEvent(new Event('submit'));
    // Switch to naturalist tab
    document.querySelector('[data-tab="tab-naturalist"]')?.click();
  }
}
window.askQuestion = askQuestion;
