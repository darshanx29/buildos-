// BuildOS — Shared API client
// All pages import this to talk to the Flask backend

const BASE = 'http://localhost:5000/api';

// ── Projects ──────────────────────────────────────────────
async function getProjects() {
  const r = await fetch(`${BASE}/projects/`);
  return r.json();
}

async function getProject(id) {
  const r = await fetch(`${BASE}/projects/${id}`);
  return r.json();
}

// ── Materials ─────────────────────────────────────────────
async function getMaterials(projectId) {
  const r = await fetch(`${BASE}/materials/${projectId}`);
  return r.json();
}

async function getLowStock(projectId) {
  const r = await fetch(`${BASE}/materials/low-stock/${projectId}`);
  return r.json();
}

async function addMaterial(data) {
  const r = await fetch(`${BASE}/materials/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return r.json();
}

async function deleteMaterial(id) {
  const r = await fetch(`${BASE}/materials/${id}`, { method: 'DELETE' });
  return r.json();
}

// ── Transactions ──────────────────────────────────────────
async function getTransactions(projectId) {
  const r = await fetch(`${BASE}/transactions/${projectId}`);
  return r.json();
}

async function logTransaction(data) {
  const r = await fetch(`${BASE}/transactions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!r.ok) {
    const err = await r.json();
    throw new Error(err.error || 'Transaction failed');
  }
  return r.json();
}

// ── Budget ────────────────────────────────────────────────
async function getBudget(projectId) {
  const r = await fetch(`${BASE}/budget/${projectId}`);
  return r.json();
}

// ── Invoices ──────────────────────────────────────────────
async function getInvoices(projectId) {
  const r = await fetch(`${BASE}/invoices/${projectId}`);
  return r.json();
}

async function createInvoice(projectId, items) {
  const r = await fetch(`${BASE}/invoices/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: projectId, items })
  });
  return r.json();
}

async function updateInvoiceStatus(invoiceId, status) {
  const r = await fetch(`${BASE}/invoices/${invoiceId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  });
  return r.json();
}

// ── Helpers ───────────────────────────────────────────────
function fmt(n) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(n);
}

function timeAgo(dateStr) {
  const diff = (Date.now() - new Date(dateStr)) / 1000;
  if (diff < 3600) return Math.floor(diff / 60) + ' mins ago';
  if (diff < 86400) return Math.floor(diff / 3600) + ' hours ago';
  return Math.floor(diff / 86400) + ' days ago';
}

function showToast(msg, type = 'success') {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = `fixed bottom-24 md:bottom-8 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-xl text-sm font-bold shadow-lg transition-all duration-300 ${type === 'error' ? 'bg-red-600 text-white' : 'bg-on-surface text-white'}`;
  t.style.opacity = '1';
  setTimeout(() => { t.style.opacity = '0'; }, 3000);
}

// Active project stored in localStorage
function getActiveProject() {
  return localStorage.getItem('buildos_project_id');
}
function setActiveProject(id) {
  localStorage.setItem('buildos_project_id', id);
}
