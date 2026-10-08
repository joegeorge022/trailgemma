/**
 * TabPFN Foundation Model UI Renderer — Clean professional output components
 */
const TabPFNUI = {
  renderFostPrediction(containerId, data) {
    this.renderFrostPrediction(containerId, data);
  },

  renderFrostPrediction(containerId, data) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const probs = data.probabilities || { safe: 0.8, light_frost: 0.15, hard_freeze: 0.05 };
    const advice = data.garden_advice || {};
    const catId = data.predicted_category_id ?? 0;

    const catColors = ['var(--accent)', 'var(--warn)', 'var(--danger)'];
    const catColor = catColors[catId] || 'var(--accent)';

    const bars = [
      { label: 'No frost risk', val: probs.safe,        color: 'var(--accent)' },
      { label: 'Light frost',   val: probs.light_frost, color: 'var(--warn)'   },
      { label: 'Hard freeze',   val: probs.hard_freeze, color: 'var(--danger)' },
    ];

    el.innerHTML = `
      <div class="stat-grid" style="margin-bottom: 1.25rem;">
        <div class="stat-cell">
          <div class="stat-label">Prediction</div>
          <div class="stat-value" style="font-size: 0.95rem; color: ${catColor}; letter-spacing: -0.01em;">
            ${data.category_name || '—'}
          </div>
        </div>
        <div class="stat-cell">
          <div class="stat-label">Days until frost</div>
          <div class="stat-value" style="color: ${catColor};">${data.estimated_days_until_frost ?? '—'}</div>
        </div>
        <div class="stat-cell">
          <div class="stat-label">Soil temp (est.)</div>
          <div class="stat-value">${data.soil_temperature_est_c ?? '—'}<span style="font-size: 0.65rem; color: var(--text-3);">°C</span></div>
        </div>
        <div class="stat-cell">
          <div class="stat-label">Night low</div>
          <div class="stat-value">${(data.inputs || {}).avg_night_temp_c ?? '—'}<span style="font-size: 0.65rem; color: var(--text-3);">°C</span></div>
        </div>
      </div>

      <div class="section-label">Probability distribution</div>
      <div class="prob-list" style="margin-bottom: 1.25rem;">
        ${bars.map(b => `
          <div class="prob-item">
            <div class="prob-label-row">
              <span class="prob-label">${b.label}</span>
              <span class="prob-pct" style="color: ${b.color};">${Math.round(b.val * 100)}%</span>
            </div>
            <div class="prob-bar">
              <div class="prob-fill" style="width: ${b.val * 100}%; background: ${b.color};"></div>
            </div>
          </div>
        `).join('')}
      </div>

      ${advice.urgency ? `
        <div class="callout ${catId === 0 ? 'callout-green' : catId === 1 ? 'callout-amber' : 'callout-red'}">
          <div class="callout-title">${advice.urgency}</div>
          ${advice.action || ''}
        </div>
      ` : ''}

      ${advice.safe_to_plant_now?.length ? `
        <div style="margin-top: 1rem;">
          <div class="section-label">Plant this week</div>
          <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.35rem;">
            ${advice.safe_to_plant_now.map(p => `<span class="tag tag-green">${p}</span>`).join('')}
          </div>
        </div>
      ` : ''}

      ${advice.harvest_immediately?.length ? `
        <div style="margin-top: 0.875rem;">
          <div class="section-label">Harvest before nightfall</div>
          <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.35rem;">
            ${advice.harvest_immediately.map(p => `<span class="tag tag-red">${p}</span>`).join('')}
          </div>
        </div>
      ` : ''}
    `;
  },

  renderFoliagePrediction(containerId, data) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const probs = data.stage_probabilities || [0.1, 0.2, 0.65, 0.05];
    const stageNames  = ['Early green', 'Moderate color', 'Peak canopy', 'Past peak'];
    const stageColors = ['var(--accent)', 'var(--warn)', '#f97316', '#9a3412'];
    const stageId = data.stage_id ?? 2;

    el.innerHTML = `
      <div class="stat-grid" style="margin-bottom: 1.25rem;">
        <div class="stat-cell">
          <div class="stat-label">Canopy stage</div>
          <div class="stat-value" style="font-size: 0.85rem; color: ${stageColors[stageId]}; letter-spacing: -0.01em; line-height: 1.2;">${data.stage_name || '—'}</div>
        </div>
        <div class="stat-cell">
          <div class="stat-label">Vibrancy index</div>
          <div class="stat-value" style="color: ${stageColors[stageId]};">${data.vibrancy_index ?? '—'}<span style="font-size: 0.65rem; color: var(--text-3);">%</span></div>
        </div>
      </div>

      <div class="section-label">Stage probability</div>
      <div class="prob-list" style="margin-bottom: 1.25rem;">
        ${probs.map((p, i) => `
          <div class="prob-item">
            <div class="prob-label-row">
              <span class="prob-label">${stageNames[i]}</span>
              <span class="prob-pct" style="color: ${stageColors[i]};">${Math.round(p * 100)}%</span>
            </div>
            <div class="prob-bar">
              <div class="prob-fill" style="width: ${p * 100}%; background: ${stageColors[i]};"></div>
            </div>
          </div>
        `).join('')}
      </div>

      ${data.trail_recommendation ? `
        <div class="callout callout-green">
          ${data.trail_recommendation}
        </div>
      ` : ''}

      ${data.canopy_breakdown ? `
        <div style="margin-top: 1rem;">
          <div class="section-label">Species breakdown</div>
          <div style="display: flex; flex-direction: column; gap: 0.35rem; margin-top: 0.4rem;">
            ${Object.entries(data.canopy_breakdown).map(([k, v]) => `
              <div style="display: flex; justify-content: space-between; font-size: 0.775rem; color: var(--text-2); padding: 0.35rem 0; border-bottom: 1px solid var(--border);">
                <span style="text-transform: capitalize;">${k.replace('_', ' ')}</span>
                <span style="color: var(--text-1);">${v}</span>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}
    `;
  },

  renderBirdPrediction(containerId, data) {
    const els = [document.getElementById(containerId), document.getElementById('tabpfn-bird-results-full')];
    const birds = data.top_species || [];

    const html = birds.length ? `
      <div class="bird-list">
        ${birds.map(b => `
          <div class="bird-item">
            <div>
              <div class="bird-name">${b.name}</div>
              <div class="bird-call">"${b.call}"</div>
              <div class="bird-tip">${b.activity}</div>
            </div>
            <div class="bird-pct">${Math.round(b.probability * 100)}%</div>
          </div>
        `).join('')}
      </div>
      ${data.listening_tip ? `<p style="font-size: 0.75rem; color: var(--text-3); margin-top: 0.875rem; line-height: 1.5;">${data.listening_tip}</p>` : ''}
    ` : `<div class="empty-state"><p>No predictions available.</p></div>`;

    els.forEach(el => { if (el) el.innerHTML = html; });
  }
};

window.TabPFNUI = TabPFNUI;
