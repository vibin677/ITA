// AgroPredict AI - Frontend Application Logic

let currentTab = 'predict';
let sensitivityChartInstance = null;
let importanceChartInstance = null;
let suitabilityChartInstance = null;
let lastPredictionData = null;
let currentDatasetPage = 1;
let batchCsvDownloadData = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', async () => {
    initTabNavigation();
    initSliderSync();
    await loadInitialData();
    initPredictionForm();
    initSensitivityTab();
    initDatasetExplorer();
    initBatchUpload();
});

// Tab Navigation
function initTabNavigation() {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            const target = tab.getAttribute('data-tab');
            switchTab(target);
        });
    });
}

function switchTab(tabId) {
    currentTab = tabId;
    document.querySelectorAll('.nav-tab').forEach(t => {
        if (t.getAttribute('data-tab') === tabId) {
            t.classList.add('active');
        } else {
            t.classList.remove('active');
        }
    });

    document.querySelectorAll('.tab-content').forEach(section => {
        if (section.id === `tab-${tabId}`) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    });

    if (tabId === 'leaderboard' && !importanceChartInstance) {
        renderLeaderboardCharts();
    }
    if (tabId === 'sensitivity') {
        runSensitivityAnalysis();
    }
    if (tabId === 'dataset') {
        loadDatasetRecords(1);
    }
}

// Input and Slider Synchronization
function initSliderSync() {
    const pairs = [
        ['input-rainfall', 'slider-rainfall', 'val-rainfall', ' mm'],
        ['input-temp', 'slider-temp', 'val-temp', ' °C'],
        ['input-fertilizer', 'slider-fertilizer', 'val-fertilizer', ' kg/ha'],
        ['input-pesticide', 'slider-pesticide', 'val-pesticide', ' kg/ha']
    ];

    pairs.forEach(([inputId, sliderId, displayId, unit]) => {
        const input = document.getElementById(inputId);
        const slider = document.getElementById(sliderId);
        const display = document.getElementById(displayId);

        if (input && slider) {
            input.addEventListener('input', () => {
                slider.value = input.value;
                if (display) display.textContent = input.value + unit;
            });
            slider.addEventListener('input', () => {
                input.value = slider.value;
                if (display) display.textContent = slider.value + unit;
            });
        }
    });
}

// Load metadata, stats, presets
async function loadInitialData() {
    try {
        const [healthRes, presetsRes, comparisonRes, statsRes] = await Promise.all([
            fetch('/api/health').then(r => r.json()),
            fetch('/api/presets').then(r => r.json()),
            fetch('/api/models/comparison').then(r => r.json()),
            fetch('/api/dataset/stats').then(r => r.json())
        ]);

        // Update Header status
        const modelBadge = document.getElementById('header-model-badge');
        if (modelBadge && healthRes.model_name) {
            modelBadge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 inline-block mr-1.5 animate-pulse"></span>Model: <strong>${healthRes.model_name}</strong> (R²: ${healthRes.champion_r2})`;
        }

        // Populate Presets Pills
        renderPresetPills(presetsRes);

        // Store comparison & stats globally
        window._modelData = comparisonRes;
        window._statsData = statsRes;

        // Populate options in dropdowns if available
        if (comparisonRes.crops) {
            populateSelect('select-crop', comparisonRes.crops);
        }
        if (comparisonRes.states) {
            populateSelect('select-state', comparisonRes.states);
            populateSelect('filter-dataset-state', comparisonRes.states, true);
        }
        if (comparisonRes.seasons) {
            populateSelect('select-season', comparisonRes.seasons);
        }
        if (comparisonRes.crops) {
            populateSelect('filter-dataset-crop', comparisonRes.crops, true);
        }

        // Render Leaderboard Table
        renderLeaderboardTable(comparisonRes.models);

        // Update Dataset overview cards
        if (statsRes.total_records) {
            document.getElementById('stat-total-records').textContent = statsRes.total_records.toLocaleString();
            document.getElementById('stat-avg-yield').textContent = `${statsRes.avg_yield} T/ha`;
            document.getElementById('stat-max-yield').textContent = `${statsRes.max_yield} T/ha`;
            document.getElementById('stat-avg-rain').textContent = `${statsRes.avg_rainfall} mm`;
        }

        // Trigger default prediction once presets are loaded
        if (presetsRes.length > 0) {
            applyPreset(presetsRes[0], false);
        }

    } catch (err) {
        console.error('Failed to load initial platform data:', err);
    }
}

function populateSelect(selectId, items, includeAll = false) {
    const el = document.getElementById(selectId);
    if (!el) return;
    const currentVal = el.value;
    el.innerHTML = '';
    if (includeAll) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'All Options';
        el.appendChild(opt);
    }
    items.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item;
        opt.textContent = item;
        el.appendChild(opt);
    });
    if (currentVal && items.includes(currentVal)) {
        el.value = currentVal;
    }
}

function renderPresetPills(presets) {
    const container = document.getElementById('preset-container');
    if (!container) return;
    container.innerHTML = '';

    presets.forEach(p => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'px-3 py-1.5 text-xs font-medium rounded-full border border-emerald-200 bg-white hover:bg-emerald-50 text-emerald-800 transition shadow-sm flex items-center space-x-1.5 whitespace-nowrap cursor-pointer';
        btn.innerHTML = `<span class="text-emerald-500 font-bold">✦</span> <span>${p.title}</span>`;
        btn.title = p.desc;
        btn.addEventListener('click', () => {
            applyPreset(p, true);
        });
        container.appendChild(btn);
    });
}

function applyPreset(p, triggerPredict = true) {
    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) {
            el.value = val;
            el.dispatchEvent(new Event('input'));
        }
    };

    setVal('select-crop', p.crop);
    setVal('select-state', p.state);
    setVal('select-season', p.season);
    setVal('input-area', p.area);
    setVal('input-rainfall', p.rainfall);
    setVal('input-temp', p.temperature);
    setVal('input-fertilizer', p.fertilizer);
    setVal('input-pesticide', p.pesticide);

    if (triggerPredict) {
        predictYield();
    }
}

// Prediction Form
function initPredictionForm() {
    const form = document.getElementById('crop-prediction-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            predictYield();
        });
    }

    // Quick area buttons
    document.querySelectorAll('.btn-area-add').forEach(btn => {
        btn.addEventListener('click', () => {
            const addVal = parseFloat(btn.getAttribute('data-add') || 0);
            const input = document.getElementById('input-area');
            if (input) {
                input.value = Math.max(1, Math.round(parseFloat(input.value || 0) + addVal));
            }
        });
    });
}

function getFormData() {
    return {
        crop: document.getElementById('select-crop').value,
        state: document.getElementById('select-state').value,
        season: document.getElementById('select-season').value,
        area: parseFloat(document.getElementById('input-area').value || 1000),
        rainfall: parseFloat(document.getElementById('input-rainfall').value || 800),
        temperature: parseFloat(document.getElementById('input-temp').value || 25),
        fertilizer: parseFloat(document.getElementById('input-fertilizer').value || 100),
        pesticide: parseFloat(document.getElementById('input-pesticide').value || 20)
    };
}

async function predictYield() {
    const payload = getFormData();
    const btn = document.getElementById('btn-submit-predict');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<svg class="animate-spin h-5 w-5 text-white inline mr-2" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Computing ML Inference...`;
    btn.disabled = true;

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Prediction failed');
        }

        const data = await res.json();
        lastPredictionData = data;
        renderPredictionResults(data);

    } catch (err) {
        alert(`Prediction Error: ${err.message}`);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function renderPredictionResults(data) {
    const resultsContainer = document.getElementById('prediction-results-card');
    resultsContainer.classList.remove('opacity-50', 'pointer-events-none');

    // Smooth counter animation
    animateValue('res-yield-value', 0, data.predicted_yield_tonnes_per_ha, 800, ' T/ha');
    animateValue('res-production-value', 0, data.total_production_tonnes, 800, ' Tonnes');

    // Yield category badge
    const badge = document.getElementById('res-category-badge');
    badge.textContent = data.advisory.category;
    badge.className = `px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider inline-flex items-center gap-1.5 bg-${data.advisory.category_badge}-100 text-${data.advisory.category_badge}-800 border border-${data.advisory.category_badge}-300`;

    // Suitability Score
    const scoreVal = document.getElementById('res-suitability-score');
    if (scoreVal) scoreVal.textContent = `${data.suitability_score}/100`;
    const scoreBar = document.getElementById('res-suitability-bar');
    if (scoreBar) scoreBar.style.width = `${data.suitability_score}%`;

    // Economics breakdown
    const eco = data.economics;
    document.getElementById('res-msp-rate').textContent = `₹${eco.msp_rate_per_tonne_inr.toLocaleString()} / Tonne ($${eco.msp_rate_per_tonne_usd})`;
    document.getElementById('res-gross-revenue').textContent = `₹${eco.gross_revenue_inr.toLocaleString()}`;
    document.getElementById('res-gross-revenue-usd').textContent = `≈ $${eco.gross_revenue_usd.toLocaleString()}`;
    document.getElementById('res-total-cost').textContent = `₹${eco.total_cost_inr.toLocaleString()}`;
    document.getElementById('res-net-profit').textContent = `₹${eco.net_profit_inr.toLocaleString()}`;
    document.getElementById('res-roi').textContent = `${eco.roi_percentage}% ROI`;

    // Agronomic Diagnostic status cards
    const adv = data.advisory;
    renderDiagnosticPill('diag-rainfall', adv.rainfall_eval.status, adv.rainfall_eval.note);
    renderDiagnosticPill('diag-temp', adv.temperature_eval.status, adv.temperature_eval.note);
    renderDiagnosticPill('diag-fertilizer', adv.fertilizer_eval.status, adv.fertilizer_eval.note);
    renderDiagnosticPill('diag-pesticide', adv.pesticide_eval.status, adv.pesticide_eval.note);

    // Advisory Recommendations List
    const recList = document.getElementById('res-advisory-list');
    recList.innerHTML = '';
    adv.recommendations.forEach(r => {
        const li = document.createElement('li');
        li.className = 'text-xs text-slate-700 flex items-start gap-2';
        li.innerHTML = `<span class="text-emerald-600 font-bold mt-0.5">✓</span><span>${r}</span>`;
        recList.appendChild(li);
    });

    // Render Radar Suitability Chart
    renderSuitabilityRadar(data.radar_metrics);
}

function renderDiagnosticPill(elementId, status, note) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.innerHTML = `
        <div class="font-semibold text-slate-900 text-xs">${status}</div>
        <div class="text-[11px] text-slate-500 mt-0.5">${note}</div>
    `;
}

function renderSuitabilityRadar(metrics) {
    const canvas = document.getElementById('chart-suitability-radar');
    if (!canvas) return;

    const labels = Object.keys(metrics);
    const values = Object.values(metrics);

    if (suitabilityChartInstance) {
        suitabilityChartInstance.destroy();
    }

    suitabilityChartInstance = new Chart(canvas, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Agro-climatic Fit Score',
                data: values,
                backgroundColor: 'rgba(16, 185, 129, 0.25)',
                borderColor: '#059669',
                pointBackgroundColor: '#047857',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#059669',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(226, 232, 240, 0.8)' },
                    grid: { color: 'rgba(226, 232, 240, 0.8)' },
                    pointLabels: {
                        font: { size: 10, family: 'Plus Jakarta Sans', weight: '600' },
                        color: '#475569'
                    },
                    suggestedMin: 20,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function animateValue(id, start, end, duration, suffix = '') {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = (progress * (end - start)) + start;
        obj.innerHTML = current.toLocaleString(undefined, {
            minimumFractionDigits: end % 1 === 0 ? 0 : 2,
            maximumFractionDigits: end % 1 === 0 ? 0 : 2
        }) + suffix;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}


// Sensitivity Simulator
function initSensitivityTab() {
    const radioInputs = document.querySelectorAll('input[name="sensitivity-param"]');
    radioInputs.forEach(r => {
        r.addEventListener('change', () => {
            runSensitivityAnalysis();
        });
    });
}

async function runSensitivityAnalysis() {
    const formBase = getFormData();
    const activeRadio = document.querySelector('input[name="sensitivity-param"]:checked');
    const param = activeRadio ? activeRadio.value : 'rainfall';

    try {
        const res = await fetch('/api/predict/sensitivity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                base_request: formBase,
                parameter: param
            })
        });

        if (!res.ok) throw new Error('Failed to run sensitivity analysis');
        const data = await res.json();
        renderSensitivityChart(data);
        renderSensitivityTable(data);

    } catch (err) {
        console.error('Sensitivity error:', err);
    }
}

function renderSensitivityChart(data) {
    const canvas = document.getElementById('chart-sensitivity');
    if (!canvas) return;

    const labels = data.curve.map(d => `${d.delta_pct} (${d.value})`);
    const yieldValues = data.curve.map(d => d.predicted_yield);

    if (sensitivityChartInstance) {
        sensitivityChartInstance.destroy();
    }

    sensitivityChartInstance = new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Predicted Yield (T/ha) vs ${data.parameter.toUpperCase()}`,
                data: yieldValues,
                borderColor: '#059669',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: labels.map((l, i) => i === 3 ? '#f59e0b' : '#059669'),
                pointRadius: labels.map((l, i) => i === 3 ? 8 : 5),
                tension: 0.35,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        afterLabel: function(ctx) {
                            const point = data.curve[ctx.dataIndex];
                            return `Total Production: ${point.total_production.toLocaleString()} Tonnes`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    title: { display: true, text: 'Yield (Tonnes / Hectare)' },
                    grid: { color: '#f1f5f9' }
                },
                x: {
                    title: { display: true, text: `Variation in ${data.parameter} from current setting` },
                    grid: { color: '#f8fafc' }
                }
            }
        }
    });
}

function renderSensitivityTable(data) {
    const tbody = document.getElementById('sensitivity-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    data.curve.forEach((item, idx) => {
        const tr = document.createElement('tr');
        const isBase = idx === 3;
        tr.className = isBase ? 'bg-amber-50 font-semibold text-amber-900 border-l-4 border-amber-500' : 'hover:bg-slate-50';
        tr.innerHTML = `
            <td class="px-4 py-2.5 text-xs">${item.delta_pct} ${isBase ? '<span class="text-[10px] bg-amber-200 text-amber-800 px-1.5 py-0.5 rounded ml-1">BASELINE</span>' : ''}</td>
            <td class="px-4 py-2.5 text-xs">${item.value}</td>
            <td class="px-4 py-2.5 text-xs text-emerald-700 font-medium">${item.predicted_yield} T/ha</td>
            <td class="px-4 py-2.5 text-xs text-slate-800">${item.total_production.toLocaleString()} Tonnes</td>
        `;
        tbody.appendChild(tr);
    });
}


// Leaderboard & Feature Importance
function renderLeaderboardTable(models) {
    const tbody = document.getElementById('leaderboard-table-body');
    if (!tbody || !models) return;
    tbody.innerHTML = '';

    models.forEach((m, idx) => {
        const tr = document.createElement('tr');
        const isChamp = idx === 0;
        tr.className = isChamp ? 'bg-emerald-50/70 font-semibold border-l-4 border-emerald-500' : 'hover:bg-slate-50';
        tr.innerHTML = `
            <td class="px-4 py-3 text-xs flex items-center gap-2">
                ${isChamp ? '<span class="text-emerald-600 text-sm">🏆</span>' : `<span class="text-slate-400 font-mono text-[11px]">#${idx+1}</span>`}
                <span class="${isChamp ? 'text-emerald-950 font-bold' : 'text-slate-700'}">${m.name}</span>
                ${isChamp ? '<span class="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-bold ml-1">CHAMPION</span>' : ''}
            </td>
            <td class="px-4 py-3 text-xs font-mono ${isChamp ? 'text-emerald-700 font-bold' : 'text-slate-800'}">${m.r2.toFixed(4)}</td>
            <td class="px-4 py-3 text-xs font-mono text-slate-600">${m.rmse.toFixed(2)}</td>
            <td class="px-4 py-3 text-xs font-mono text-slate-600">${m.mae.toFixed(2)}</td>
            <td class="px-4 py-3 text-xs font-mono text-slate-600">${m.cv_r2.toFixed(4)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderLeaderboardCharts() {
    const meta = window._modelData;
    if (!meta || !meta.feature_importances) return;

    const canvas = document.getElementById('chart-feature-importance');
    if (!canvas) return;

    const labels = meta.feature_importances.map(f => f.feature);
    const dataVals = meta.feature_importances.map(f => (f.importance * 100).toFixed(1));

    importanceChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Relative Predictive Impact (%)',
                data: dataVals,
                backgroundColor: [
                    '#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#64748b'
                ],
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` Relative Impact: ${ctx.raw}%`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Importance Contribution (%)' },
                    grid: { color: '#f1f5f9' },
                    max: 100
                },
                y: { grid: { display: false } }
            }
        }
    });
}


// Dataset Explorer
function initDatasetExplorer() {
    const searchInput = document.getElementById('input-dataset-search');
    const cropFilter = document.getElementById('filter-dataset-crop');
    const stateFilter = document.getElementById('filter-dataset-state');

    let debounceTimer;
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                loadDatasetRecords(1);
            }, 300);
        });
    }

    if (cropFilter) cropFilter.addEventListener('change', () => loadDatasetRecords(1));
    if (stateFilter) stateFilter.addEventListener('change', () => loadDatasetRecords(1));

    const prevBtn = document.getElementById('btn-dataset-prev');
    const nextBtn = document.getElementById('btn-dataset-next');

    if (prevBtn) prevBtn.addEventListener('click', () => {
        if (currentDatasetPage > 1) loadDatasetRecords(currentDatasetPage - 1);
    });
    if (nextBtn) nextBtn.addEventListener('click', () => {
        loadDatasetRecords(currentDatasetPage + 1);
    });
}

async function loadDatasetRecords(page = 1) {
    currentDatasetPage = page;
    const search = document.getElementById('input-dataset-search')?.value || '';
    const crop = document.getElementById('filter-dataset-crop')?.value || '';
    const state = document.getElementById('filter-dataset-state')?.value || '';

    const params = new URLSearchParams({
        page: page,
        page_size: 12,
        search: search,
        crop: crop,
        state: state
    });

    try {
        const res = await fetch(`/api/dataset/records?${params.toString()}`);
        const data = await res.json();
        renderDatasetTable(data);
    } catch (err) {
        console.error('Failed to load dataset records:', err);
    }
}

function renderDatasetTable(data) {
    const tbody = document.getElementById('dataset-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (!data.records || data.records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center py-8 text-xs text-slate-400">No matching records found in crop dataset.</td></tr>`;
        return;
    }

    data.records.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 border-b border-slate-100 transition';
        tr.innerHTML = `
            <td class="px-3 py-2 text-xs font-semibold text-slate-800">${r.Crop}</td>
            <td class="px-3 py-2 text-xs text-slate-600">${r.State}</td>
            <td class="px-3 py-2 text-xs text-slate-600"><span class="px-2 py-0.5 bg-slate-100 rounded text-[11px]">${r.Season}</span></td>
            <td class="px-3 py-2 text-xs font-mono text-slate-600">${r.Area.toLocaleString()}</td>
            <td class="px-3 py-2 text-xs font-mono text-slate-600">${r.Rainfall}</td>
            <td class="px-3 py-2 text-xs font-mono text-slate-600">${r.Temperature}°C</td>
            <td class="px-3 py-2 text-xs font-mono text-slate-600">${r.Fertilizer}</td>
            <td class="px-3 py-2 text-xs font-mono text-slate-600">${r.Pesticide}</td>
            <td class="px-3 py-2 text-xs font-mono font-bold text-emerald-700 bg-emerald-50/50">${r.Yield}</td>
        `;
        tbody.appendChild(tr);
    });

    // Pagination info
    const info = document.getElementById('dataset-page-info');
    if (info) {
        info.textContent = `Page ${data.page} of ${data.total_pages} (${data.total.toLocaleString()} total rows)`;
    }

    const prevBtn = document.getElementById('btn-dataset-prev');
    const nextBtn = document.getElementById('btn-dataset-next');
    if (prevBtn) prevBtn.disabled = data.page <= 1;
    if (nextBtn) nextBtn.disabled = data.page >= data.total_pages;
}


// Batch CSV Predictor
function initBatchUpload() {
    const fileInput = document.getElementById('input-batch-file');
    const dropZone = document.getElementById('batch-drop-zone');
    const btnSample = document.getElementById('btn-download-sample-csv');
    const btnDownloadResults = document.getElementById('btn-download-batch-results');

    if (btnSample) {
        btnSample.addEventListener('click', downloadSampleCsv);
    }

    if (dropZone && fileInput) {
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-emerald-500', 'bg-emerald-50/50');
        });
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-emerald-500', 'bg-emerald-50/50');
        });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-emerald-500', 'bg-emerald-50/50');
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                processBatchFile(e.dataTransfer.files[0]);
            }
        });
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                processBatchFile(fileInput.files[0]);
            }
        });
    }

    if (btnDownloadResults) {
        btnDownloadResults.addEventListener('click', () => {
            if (!batchCsvDownloadData) return;
            const blob = new Blob([batchCsvDownloadData], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `crop_yield_batch_predictions_${Date.now()}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }
}

async function processBatchFile(file) {
    if (!file.name.endsWith('.csv')) {
        alert('Please upload a valid .csv file.');
        return;
    }

    const statusEl = document.getElementById('batch-status-text');
    statusEl.innerHTML = `<span class="text-emerald-600 font-semibold">Processing batch predictions for ${file.name}...</span>`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/api/predict/batch', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Batch processing failed');
        }

        const data = await res.json();
        batchCsvDownloadData = data.csv_data;

        statusEl.innerHTML = `
            <span class="text-emerald-700 font-bold">✓ Successfully processed ${data.total_rows_processed} records!</span>
            <div class="text-xs text-slate-600 mt-1">
                Average Predicted Yield: <strong>${data.summary.average_predicted_yield_tonnes_ha} T/ha</strong> | 
                Total Estimated Production: <strong>${data.summary.total_batch_production_tonnes.toLocaleString()} Tonnes</strong>
            </div>
        `;

        document.getElementById('batch-results-panel').classList.remove('hidden');
        renderBatchPreviewTable(data.preview_rows);

    } catch (err) {
        statusEl.innerHTML = `<span class="text-rose-600 font-semibold">Error: ${err.message}</span>`;
    }
}

function renderBatchPreviewTable(rows) {
    const tbody = document.getElementById('batch-preview-table-body');
    if (!tbody || !rows) return;
    tbody.innerHTML = '';

    rows.slice(0, 15).forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 border-b border-slate-100 text-xs';
        tr.innerHTML = `
            <td class="px-3 py-2 font-semibold">${r.Crop}</td>
            <td class="px-3 py-2 text-slate-600">${r.State}</td>
            <td class="px-3 py-2 text-slate-600">${r.Season}</td>
            <td class="px-3 py-2 font-mono">${r.Area}</td>
            <td class="px-3 py-2 font-mono font-bold text-emerald-700 bg-emerald-50">${r.Predicted_Yield_Tonnes_Ha} T/ha</td>
            <td class="px-3 py-2 font-mono font-bold text-slate-900">${r.Total_Production_Tonnes.toLocaleString()} T</td>
        `;
        tbody.appendChild(tr);
    });
}

function downloadSampleCsv() {
    const sample = `Area,Rainfall,Temperature,Fertilizer,Pesticide,State,Crop,Season\n1200,680,18.5,130,15,Punjab,Wheat,Rabi\n2200,850,29.0,110,35,Maharashtra,Cotton,Kharif\n1800,1200,28.5,125,25,Tamil Nadu,Rice,Kharif\n2500,1150,28.0,160,30,Uttar Pradesh,Sugarcane,Whole Year\n800,650,24.0,90,20,Karnataka,Maize,Kharif`;
    const blob = new Blob([sample], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'crop_yield_batch_template.csv';
    a.click();
    URL.revokeObjectURL(url);
}
