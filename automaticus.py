#!/usr/bin/env python3
"""
Automaticus — Automatic Video Generator
-----------------------------------------
Run in Google Colab:

  pip install -r requirements.txt
  python automaticus.py
"""

import threading
import requests
import json
import time
import os
import re
from mutagen.mp3 import MP3
import urllib.request
from flask import Flask, request, jsonify
from flask_cors import CORS

    pass
except:
    pass

app = Flask(__name__)
CORS(app)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Automaticus — Automatic Video Generator</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #fafaf8;
    --surface: #ffffff;
    --surface2: #f5f4f0;
    --border: #e8e5de;
    --border-dark: #d0ccc2;
    --text: #1a1916;
    --text-mid: #5a5750;
    --text-muted: #9a9690;
    --accent: #2c4a3e;
    --accent-light: #4a7a68;
    --accent-pale: #e8f0ed;
    --gold: #b8965a;
    --gold-pale: #f5f0e8;
    --red: #8b2020;
    --green: #2c4a3e;
    --green-text: #2c7a5a;
    --serif: 'Cormorant Garamond', Georgia, serif;
    --sans: 'Inter', system-ui, sans-serif;
    --radius: 6px;
  }

  html { background: var(--bg); color: var(--text); font-family: var(--sans); font-size: 14px; }
  body { min-height: 100vh; display: flex; flex-direction: column; }

  /* HEADER */
  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1.25rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
  }

  .brand-name {
    font-family: var(--serif);
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.04em;
  }

  .brand-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--gold);
    margin-bottom: 3px;
    flex-shrink: 0;
  }

  .brand-tagline {
    font-size: 11px;
    font-weight: 300;
    color: var(--text-muted);
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .header-right {
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* MAIN LAYOUT */
  .main {
    display: grid;
    grid-template-columns: 400px 1fr;
    flex: 1;
    min-height: 0;
  }

  /* LEFT PANEL */
  .panel-left {
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    overflow-y: auto;
  }

  .panel-section-title {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
  }

  .field-group { display: flex; flex-direction: column; gap: 0.45rem; }

  label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: var(--text-mid);
  }

  input[type="text"],
  input[type="password"],
  textarea,
  select {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: var(--sans);
    font-size: 13px;
    font-weight: 300;
    padding: 0.6rem 0.85rem;
    border-radius: var(--radius);
    width: 100%;
    transition: border-color 0.15s, box-shadow 0.15s;
    outline: none;
    line-height: 1.5;
  }

  input:focus, textarea:focus, select:focus {
    border-color: var(--accent-light);
    box-shadow: 0 0 0 3px rgba(74,122,104,0.08);
    background: var(--surface);
  }

  textarea {
    resize: vertical;
    min-height: 100px;
    line-height: 1.7;
  }

  .hint {
    font-size: 11px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.6;
  }

  .hint a {
    color: var(--accent-light);
    text-decoration: none;
  }

  .hint a:hover { text-decoration: underline; }

  .divider {
    border: none;
    border-top: 1px solid var(--border);
  }

  /* VIDEO TYPE PILLS */
  .type-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }

  .type-pill {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.5rem 0.75rem;
    font-size: 11px;
    font-weight: 400;
    color: var(--text-mid);
    cursor: pointer;
    background: var(--surface2);
    text-align: center;
    transition: all 0.15s;
    user-select: none;
  }

  .type-pill:hover {
    border-color: var(--accent-light);
    color: var(--accent);
  }

  .type-pill.selected {
    background: var(--accent-pale);
    border-color: var(--accent-light);
    color: var(--accent);
    font-weight: 500;
  }

  /* GENERATE BUTTON */
  .btn-generate {
    background: var(--accent);
    color: #fff;
    border: none;
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.9rem 1.5rem;
    border-radius: var(--radius);
    cursor: pointer;
    width: 100%;
    transition: background 0.15s, transform 0.1s;
    margin-top: 0.25rem;
  }

  .btn-generate:hover { background: var(--accent-light); }
  .btn-generate:active { transform: scale(0.99); }
  .btn-generate:disabled { background: var(--border-dark); cursor: not-allowed; }

  /* PROGRESS */
  .progress-wrap {
    background: var(--surface2);
    border-radius: 100px;
    height: 3px;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--gold));
    transition: width 0.5s ease;
    width: 0%;
    border-radius: 100px;
  }

  /* RIGHT PANEL */
  .panel-right {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg);
  }

  /* TABS */
  .tabs {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    display: flex;
    gap: 0.25rem;
  }

  .tab {
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 1rem 0.75rem;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    background: none;
    font-family: var(--sans);
    transition: color 0.15s;
    margin-bottom: -1px;
    white-space: nowrap;
  }

  .tab:hover { color: var(--text-mid); }

  .tab.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
    font-weight: 500;
  }

  .tab-content {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    display: none;
  }

  .tab-content.active { display: block; }

  /* STEP INDICATOR */
  .steps {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 1.5rem;
  }

  .step {
    text-align: center;
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0.65rem 0.5rem;
    border-right: 1px solid var(--border);
    transition: all 0.2s;
  }

  .step:last-child { border-right: none; }
  .step.done { background: var(--accent-pale); color: var(--green-text); font-weight: 500; }
  .step.active { background: var(--gold-pale); color: var(--gold); font-weight: 500; }

  /* LOG */
  .log {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    line-height: 2;
    min-height: 240px;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--text-mid);
  }

  .log .ok { color: var(--green-text); }
  .log .err { color: var(--red); }
  .log .info { color: var(--accent); font-weight: 500; }
  .log .dim { color: var(--text-muted); }

  /* SCENES */
  .scenes-list { display: flex; flex-direction: column; gap: 1rem; }

  .scene-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
  }

  .scene-head {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.25rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
  }

  .scene-num {
    font-size: 10px;
    font-weight: 500;
    background: var(--surface);
    color: var(--text-muted);
    padding: 2px 8px;
    border-radius: 100px;
    border: 1px solid var(--border);
    white-space: nowrap;
    letter-spacing: 0.06em;
  }

  .scene-title {
    font-size: 13px;
    font-weight: 400;
    color: var(--text);
  }

  .scene-kws {
    padding: 0.65rem 1.25rem;
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    border-bottom: 1px solid var(--border);
  }

  .kw {
    font-size: 10px;
    background: var(--surface2);
    color: var(--text-muted);
    padding: 2px 8px;
    border-radius: 100px;
    border: 1px solid var(--border);
  }

  .scene-clips {
    padding: 0.75rem 1.25rem;
    display: flex;
    gap: 8px;
    overflow-x: auto;
  }

  .clip-thumb {
    flex-shrink: 0;
    width: 110px;
    height: 68px;
    border-radius: 4px;
    overflow: hidden;
    background: var(--surface2);
    border: 1px solid var(--border);
    position: relative;
  }

  .clip-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }

  .clip-dur {
    position: absolute;
    bottom: 3px; right: 4px;
    font-size: 9px;
    background: rgba(0,0,0,0.55);
    color: #fff;
    padding: 1px 4px;
    border-radius: 3px;
  }

  /* SCRIPT */
  .script-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 2rem;
    font-family: var(--serif);
    font-size: 15px;
    font-weight: 300;
    line-height: 1.9;
    white-space: pre-wrap;
    max-height: 500px;
    overflow-y: auto;
    color: var(--text);
  }

  /* TTS */
  .tts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .tts-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
  }

  .tts-card h3 {
    font-family: var(--serif);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 0.4rem;
  }

  .tts-card p {
    font-size: 12px;
    font-weight: 300;
    color: var(--text-mid);
    line-height: 1.6;
    margin-bottom: 0.6rem;
  }

  .tts-tag {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 100px;
    letter-spacing: 0.06em;
    font-weight: 500;
  }

  .tag-free { background: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; }
  .tag-paid { background: var(--gold-pale); color: var(--gold); border: 1px solid #e0d0b0; }

  .tts-card a {
    display: inline-block;
    margin-top: 0.5rem;
    font-size: 11px;
    color: var(--accent-light);
    text-decoration: none;
    letter-spacing: 0.04em;
  }

  .tts-card a:hover { text-decoration: underline; }

  .info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    font-size: 12px;
    font-weight: 300;
    color: var(--text-mid);
    line-height: 1.9;
  }

  .info-card h4 {
    font-family: var(--serif);
    font-size: 1rem;
    color: var(--accent);
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  code {
    font-family: 'Courier New', monospace;
    font-size: 11px;
    background: var(--surface2);
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid var(--border);
    color: var(--accent);
  }

  /* DOWNLOAD */
  .download-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.25rem;
  }

  .download-icon {
    font-family: var(--serif);
    font-size: 3rem;
    color: var(--gold);
    font-style: italic;
    line-height: 1;
  }

  .download-box h2 {
    font-family: var(--serif);
    font-size: 1.6rem;
    font-weight: 400;
    color: var(--accent);
    font-style: italic;
  }

  .download-box p {
    font-size: 12px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 360px;
  }

  .btn-download {
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--accent);
    font-family: var(--sans);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.75rem 2.5rem;
    border-radius: var(--radius);
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: all 0.15s;
  }

  .btn-download:hover {
    background: var(--accent);
    color: #fff;
  }

  .empty-state {
    font-size: 12px;
    font-weight: 300;
    font-style: italic;
    color: var(--text-muted);
    padding: 2rem 0;
    text-align: center;
  }

  @media (max-width: 900px) {
    .main { grid-template-columns: 1fr; }
    .panel-left { border-right: none; border-bottom: 1px solid var(--border); }
    .tts-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header>
  <div class="brand">
    <span class="brand-name">Automaticus</span>
    <div class="brand-dot"></div>
    <span class="brand-tagline">Automatic Video Generator</span>
  </div>
  <span class="header-right">Powered by Claude · Pexels · Shotstack</span>
</header>

<div class="main">

  <!-- LEFT PANEL -->
  <div class="panel-left">

    <div>
      <div class="panel-section-title">Video Content</div>
    </div>

    <div class="field-group">
      <label>Video Type</label>
      <div class="type-grid" id="type-grid">
        <div class="type-pill selected" onclick="selectType(this, 'horror narration')">Horror Narration</div>
        <div class="type-pill" onclick="selectType(this, 'true crime documentary')">True Crime</div>
        <div class="type-pill" onclick="selectType(this, 'educational explainer')">Educational</div>
        <div class="type-pill" onclick="selectType(this, 'travel documentary')">Travel Doc</div>
        <div class="type-pill" onclick="selectType(this, 'motivational')">Motivational</div>
        <div class="type-pill" onclick="selectType(this, 'history documentary')">History</div>
        <div class="type-pill" onclick="selectType(this, 'mystery investigation')">Mystery</div>
        <div class="type-pill" onclick="selectType(this, 'nature documentary')">Nature Doc</div>
      </div>
    </div>

    <div class="field-group">
      <label>What is this video about?</label>
      <textarea id="topic" placeholder="e.g. Four true stories of people who received terrifying messages from unknown numbers..."></textarea>
    </div>

    <div class="field-group">
      <label>Number of Stories / Segments</label>
      <select id="num-stories">
        <option value="2">2 segments</option>
        <option value="3">3 segments</option>
        <option value="4" selected>4 segments (recommended)</option>
        <option value="5">5 segments</option>
        <option value="6">6 segments</option>
      </select>
    </div>

    <hr class="divider">

    <div>
      <div class="panel-section-title">API Credentials</div>
    </div>

    <div class="field-group">
      <label>Pexels API Key</label>
      <input type="password" id="pexels-key" placeholder="••••••••••••••••" />
      <span class="hint">Free at <a href="https://www.pexels.com/api/" target="_blank">pexels.com/api</a></span>
    </div>

    <div class="field-group">
      <label>Shotstack API Key</label>
      <input type="password" id="shotstack-key" placeholder="••••••••••••••••" />
      <span class="hint">Free sandbox at <a href="https://shotstack.io" target="_blank">shotstack.io</a></span>
    </div>

    <hr class="divider">

    <div>
      <div class="panel-section-title">Voiceover</div>
    </div>

    <div class="field-group">
      <label>Audio URL</label>
      <input type="text" id="audio-url" placeholder="https://drive.google.com/uc?id=..." />
      <span class="hint">Generate with any TTS tool → upload to Google Drive → share public → use direct URL. See <a href="#" onclick="showTab('tts');return false;">TTS Tools tab</a> for options.</span>
    </div>

    <hr class="divider">

    <button class="btn-generate" id="gen-btn" onclick="startPipeline()">
      Generate Video
    </button>

    <div class="progress-wrap">
      <div class="progress-bar" id="progress"></div>
    </div>

  </div>

  <!-- RIGHT PANEL -->
  <div class="panel-right">

    <div class="tabs">
      <button class="tab active" onclick="showTab('log')">Status</button>
      <button class="tab" onclick="showTab('script')">Script</button>
      <button class="tab" onclick="showTab('scenes')">Scenes & Footage</button>
      <button class="tab" onclick="showTab('tts')">TTS Tools</button>
      <button class="tab" onclick="showTab('download')">Download</button>
    </div>

    <!-- LOG -->
    <div class="tab-content active" id="tab-log">
      <div class="steps">
        <div class="step" id="step-1">1 · Script</div>
        <div class="step" id="step-2">2 · Scenes</div>
        <div class="step" id="step-3">3 · Footage</div>
        <div class="step" id="step-4">4 · Render</div>
        <div class="step" id="step-5">5 · Complete</div>
      </div>
      <div class="log" id="log">Ready to generate.

Fill in your topic, select a video type, enter your API keys and voiceover URL, then click Generate Video.</div>
    </div>

    <!-- SCRIPT -->
    <div class="tab-content" id="tab-script">
      <div class="script-box" id="script-out"><span class="empty-state">Your generated script will appear here.</span></div>
    </div>

    <!-- SCENES -->
    <div class="tab-content" id="tab-scenes">
      <div class="scenes-list" id="scenes-out">
        <p class="empty-state">Scenes and matched footage will appear here after generation.</p>
      </div>
    </div>

    <!-- TTS TOOLS -->
    <div class="tab-content" id="tab-tts">
      <div class="tts-grid">
        <div class="tts-card">
          <h3>TTSMaker</h3>
          <p>Completely free, no account required. Paste script, choose a voice, download MP3 instantly.</p>
          <span class="tts-tag tag-free">Free · No signup</span>
          <a href="https://ttsmaker.com" target="_blank">Open TTSMaker →</a>
        </div>
        <div class="tts-card">
          <h3>Murf.ai</h3>
          <p>Best free quality. 10 minutes of audio per month free. Excellent professional narrator voices.</p>
          <span class="tts-tag tag-free">Free tier</span>
          <a href="https://murf.ai" target="_blank">Open Murf.ai →</a>
        </div>
        <div class="tts-card">
          <h3>ElevenLabs</h3>
          <p>Industry-leading voice quality. $5/mo starter covers approximately 8 full episodes per month.</p>
          <span class="tts-tag tag-paid">From $5/mo</span>
          <a href="https://try.elevenlabs.io/r426whva8n3r" target="_blank">Open ElevenLabs →</a>
        </div>
        <div class="tts-card">
          <h3>PlayHT</h3>
          <p>200+ voices with a generous free tier. Easy MP3 export, great variety of tones and styles.</p>
          <span class="tts-tag tag-free">Free tier</span>
          <a href="https://play.ht" target="_blank">Open PlayHT →</a>
        </div>
      </div>
      <div class="info-card">
        <h4>How to get your audio URL</h4>
        Generate your voiceover and download the MP3, then:<br><br>
        1. Upload the MP3 to Google Drive<br>
        2. Right-click → Share → Anyone with the link → Copy link<br>
        3. Your link will look like: <code>drive.google.com/file/d/FILE_ID/view</code><br>
        4. Change it to: <code>drive.google.com/uc?id=FILE_ID</code><br>
        5. Paste that into the Audio URL field on the left
      </div>
    </div>

    <!-- DOWNLOAD -->
    <div class="tab-content" id="tab-download">
      <div class="download-box" id="download-box">
        <div class="download-icon">A</div>
        <h2>Your video will appear here</h2>
        <p>Once generation is complete, your finished MP4 will be available to download and upload directly to YouTube or any platform.</p>
      </div>
    </div>

  </div>
</div>

<script>
let logEl = document.getElementById('log');
let progressEl = document.getElementById('progress');
let selectedType = 'horror narration';

function selectType(el, type) {
  document.querySelectorAll('.type-pill').forEach(p => p.classList.remove('selected'));
  el.classList.add('selected');
  selectedType = type;
}

function showTab(name) {
  const names = ['log','script','scenes','tts','download'];
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', names[i] === name));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
}

function log(msg, cls) {
  const line = document.createElement('span');
  line.className = cls || '';
  line.textContent = msg + '\n';
  logEl.appendChild(line);
  logEl.scrollTop = logEl.scrollHeight;
}

function setStep(n) {
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById('step-' + i);
    if (i < n) el.className = 'step done';
    else if (i === n) el.className = 'step active';
    else el.className = 'step';
  }
  progressEl.style.width = ((n-1)/4 * 100) + '%';
}

function renderScenes(scenes) {
  const out = document.getElementById('scenes-out');
  out.innerHTML = '';
  scenes.forEach(s => {
    const card = document.createElement('div');
    card.className = 'scene-card';
    const kws = (s.keywords || []).map(k => `<span class="kw">${k}</span>`).join('');
    const thumbs = (s.clips || []).slice(0,6).map(c =>
      `<div class="clip-thumb"><img src="${c.thumbnail}" loading="lazy"><span class="clip-dur">${c.duration}s</span></div>`
    ).join('');
    card.innerHTML = `
      <div class="scene-head">
        <span class="scene-num">Scene ${s.scene}</span>
        <span class="scene-title">${s.story}</span>
      </div>
      <div class="scene-kws">${kws}</div>
      ${thumbs ? `<div class="scene-clips">${thumbs}</div>` : ''}
    `;
    out.appendChild(card);
  });
}

async function startPipeline() {
  const topic = document.getElementById('topic').value.trim();
  const numStories = document.getElementById('num-stories').value;
  const pexelsKey = document.getElementById('pexels-key').value.trim();
  const shotstackKey = document.getElementById('shotstack-key').value.trim();
  const audioUrl = document.getElementById('audio-url').value.trim();

  if (!topic) { alert('Please describe what your video is about.'); return; }
  if (!pexelsKey) { alert('Please enter your Pexels API key.'); return; }
  if (!shotstackKey) { alert('Please enter your Shotstack API key.'); return; }
  if (!audioUrl) { alert('Please enter your voiceover audio URL.'); return; }

  document.getElementById('gen-btn').disabled = true;
  logEl.innerHTML = '';
  showTab('log');

  try {
    setStep(1);
    log('[ Step 1 ]  Generating script...', 'info');

    const scriptRes = await fetch('/api/generate-script', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ topic, num_stories: parseInt(numStories), video_type: selectedType })
    });
    const scriptData = await scriptRes.json();
    if (scriptData.error) throw new Error(scriptData.error);
    log('  Script generated — ' + scriptData.script.length + ' characters', 'ok');
    document.getElementById('script-out').textContent = scriptData.script;

    setStep(2);
    log('\n[ Step 2 ]  Extracting scenes and keywords...', 'info');

    const scenesRes = await fetch('/api/extract-scenes', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ script: scriptData.script, num_stories: parseInt(numStories), video_type: selectedType })
    });
    const scenesData = await scenesRes.json();
    if (scenesData.error) throw new Error(scenesData.error);
    log('  ' + scenesData.scenes.length + ' scenes extracted', 'ok');
    scenesData.scenes.forEach(s => log('  · Scene ' + s.scene + ': ' + s.story, 'dim'));

    setStep(3);
    log('\n[ Step 3 ]  Fetching stock footage from Pexels...', 'info');

    const footageRes = await fetch('/api/fetch-footage', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ scenes: scenesData.scenes, pexels_key: pexelsKey, audio_url: audioUrl })
    });
    const footageData = await footageRes.json();
    if (footageData.error) throw new Error(footageData.error);
    log('  Audio duration: ' + footageData.duration.toFixed(1) + 's (' + (footageData.duration/60).toFixed(1) + ' min)', 'ok');
    footageData.scenes.forEach(s => log('  · Scene ' + s.scene + ': ' + s.clips.length + ' clips', 'dim'));
    renderScenes(footageData.scenes);

    setStep(4);
    log('\n[ Step 4 ]  Submitting to Shotstack for rendering...', 'info');

    const renderRes = await fetch('/api/render', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        scenes: footageData.scenes,
        duration: footageData.duration,
        audio_url: audioUrl,
        shotstack_key: shotstackKey
      })
    });
    const renderData = await renderRes.json();
    if (renderData.error) throw new Error(renderData.error);
    log('  Render submitted — ID: ' + renderData.render_id, 'ok');
    log('  Polling for completion...', 'dim');

    let videoUrl = null;
    for (let i = 0; i < 60; i++) {
      await new Promise(r => setTimeout(r, 8000));
      const pollRes = await fetch('/api/poll/' + renderData.render_id + '?key=' + encodeURIComponent(shotstackKey));
      const pollData = await pollRes.json();
      log('  Status: ' + pollData.status, 'dim');
      if (pollData.status === 'done') { videoUrl = pollData.url; break; }
      if (pollData.status === 'failed') throw new Error('Render failed: ' + (pollData.error || 'unknown'));
    }

    if (!videoUrl) throw new Error('Render timed out.');

    setStep(5);
    progressEl.style.width = '100%';
    log('\n[ Complete ]  Your video is ready.', 'ok');
    log('  ' + videoUrl, 'info');

    document.getElementById('download-box').innerHTML = `
      <div class="download-icon">✓</div>
      <h2>Video Complete</h2>
      <p>Your video has been rendered and is ready to download. Upload directly to YouTube or any platform.</p>
      <a class="btn-download" href="${videoUrl}" target="_blank">Download MP4</a>
      <p style="font-size:11px;color:var(--text-muted);margin-top:0.25rem;">Link expires after 24 hours · Re-render anytime from Shotstack dashboard</p>
    `;
    showTab('download');

  } catch(err) {
    log('\n[ Error ]  ' + err.message, 'err');
    log('Please check your API keys and try again.', 'dim');
  }

  document.getElementById('gen-btn').disabled = false;
}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return HTML


@app.route('/api/generate-script', methods=['POST'])
def generate_script():
    data = request.json
    topic = data.get('topic', '')
    num_stories = data.get('num_stories', 4)
    video_type = data.get('video_type', 'documentary')

    type_instructions = {
        'horror narration': 'calm, deliberate horror narrator reading true story submissions. Dark, grounded, real-feeling.',
        'true crime documentary': 'objective, measured true crime documentary narrator. Factual, compelling, serious.',
        'educational explainer': 'clear, engaging educational narrator. Informative, accessible, enthusiastic.',
        'travel documentary': 'warm, evocative travel documentary voice. Vivid, immersive, inspiring.',
        'motivational': 'powerful, uplifting motivational narrator. Energetic, direct, inspiring.',
        'history documentary': 'authoritative, engaging history documentary narrator. Rich, detailed, dramatic.',
        'mystery investigation': 'curious, probing mystery narrator. Thoughtful, suspenseful, analytical.',
        'nature documentary': 'awe-inspired, poetic nature documentary narrator. Vivid, reverent, cinematic.',
    }

    style = type_instructions.get(video_type, 'professional, engaging narrator.')

    try:
        r = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 4000,
                'messages': [{
                    'role': 'user',
                    'content': f"""Write a long-form YouTube video script ({video_type} format) about: {topic}

Narrator style: {style}

Structure:
- Compelling opening monologue (3-4 sentences setting the theme)
- {num_stories} distinct stories or segments, each 3-5 paragraphs, in first person or narrated
- Each segment has a title on its own line in the format "Segment one. [Title]."
- Strong closing outro (2-3 sentences)
- Total length should support 8-15 minutes of narration

Write the complete script only, no meta-commentary or formatting notes."""
                }]
            }
        )
        script = r.json()['content'][0]['text']
        return jsonify({'script': script})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/extract-scenes', methods=['POST'])
def extract_scenes():
    data = request.json
    script = data.get('script', '')
    num_stories = data.get('num_stories', 4)
    video_type = data.get('video_type', 'documentary')
    num_scenes = num_stories * 2 + 2

    try:
        r = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{
                    'role': 'user',
                    'content': f"""Break this {video_type} script into exactly {num_scenes} scenes for video production.

Return ONLY a JSON array, no markdown, no explanation:
[
  {{
    "scene": 1,
    "story": "Intro",
    "description": "one sentence visual description",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "keyword6", "keyword7"]
  }}
]

Keyword rules:
- 7 per scene, all distinct
- Concrete, Pexels-searchable visual terms matching the {video_type} genre and mood
- Real-world, filmable imagery only — no abstract concepts

Script:
{script}"""
                }]
            }
        )
        raw = r.json()['content'][0]['text']
        clean = raw.replace('```json', '').replace('```', '').strip()
        scenes = json.loads(clean)
        return jsonify({'scenes': scenes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fetch-footage', methods=['POST'])
def fetch_footage():
    data = request.json
    scenes = data.get('scenes', [])
    pexels_key = data.get('pexels_key', '')
    audio_url = data.get('audio_url', '')

    try:
        urllib.request.urlretrieve(audio_url, '/tmp/vo.mp3')
        audio = MP3('/tmp/vo.mp3')
        total_duration = audio.info.length
    except Exception as e:
        return jsonify({'error': f'Could not load audio file: {str(e)}'}), 500

    clip_length = total_duration / len(scenes)
    headers = {'Authorization': pexels_key}
    enriched = []

    for s in scenes:
        needed = clip_length
        collected = []
        total = 0.0
        seen = set()

        for kw in s.get('keywords', []):
            if total >= needed:
                break
            try:
                r = requests.get(
                    'https://api.pexels.com/videos/search',
                    headers=headers,
                    params={'query': kw, 'per_page': 8, 'orientation': 'landscape'}
                )
                time.sleep(0.25)
                for v in r.json().get('videos', []):
                    if total >= needed:
                        break
                    hd = next((f for f in v.get('video_files', []) if f.get('quality') == 'hd'), None)
                    f = hd or (v.get('video_files') or [{}])[0]
                    if f.get('link') and v['id'] not in seen:
                        collected.append({
                            'id': v['id'],
                            'src': f['link'],
                            'thumbnail': v.get('image', ''),
                            'duration': v.get('duration', 10)
                        })
                        seen.add(v['id'])
                        total += v.get('duration', 10)
            except:
                pass

        enriched.append({**s, 'clips': collected})

    return jsonify({'scenes': enriched, 'duration': total_duration, 'clip_length': clip_length})


@app.route('/api/render', methods=['POST'])
def render():
    data = request.json
    scenes = data.get('scenes', [])
    total_duration = data.get('duration', 600)
    audio_url = data.get('audio_url', '')
    shotstack_key = data.get('shotstack_key', '')
    clip_length = total_duration / len(scenes)

    video_track = []
    title_track = []
    cursor = 0.0

    for i, scene in enumerate(scenes):
        scene_start = cursor
        is_last = (i == len(scenes) - 1)
        scene_len = (total_duration - cursor) if is_last else clip_length
        remaining = scene_len

        for clip in scene.get('clips', []):
            clen = min(clip['duration'], remaining)
            if clen <= 0:
                break
            video_track.append({
                'asset': {'type': 'video', 'src': clip['src'], 'volume': 0},
                'start': round(cursor, 2),
                'length': round(clen, 2),
                'transition': {'in': 'fade', 'out': 'fade'}
            })
            cursor += max(clen - 1, 0.5)
            remaining -= clen
            if remaining <= 0:
                break

        title_track.append({
            'asset': {
                'type': 'title',
                'text': scene.get('story', '').upper(),
                'style': 'minimal',
                'color': '#888888',
                'size': 'small',
                'background': 'transparent',
                'position': 'bottomLeft'
            },
            'start': round(scene_start, 2),
            'length': round(scene_len, 2),
            'transition': {'in': 'fade', 'out': 'fade'}
        })

    payload = {
        'timeline': {
            'background': '#000000',
            'tracks': [
                {'clips': video_track},
                {'clips': title_track},
                {'clips': [{'asset': {'type': 'audio', 'src': audio_url, 'volume': 1}, 'start': 0, 'length': round(total_duration, 2)}]}
            ]
        },
        'output': {'format': 'mp4', 'resolution': 'hd', 'fps': 25, 'size': {'width': 1920, 'height': 1080}}
    }

    try:
        r = requests.post(
            'https://api.shotstack.io/stage/render',
            headers={'x-api-key': shotstack_key, 'Content-Type': 'application/json'},
            json=payload
        )
        if r.status_code != 201:
            return jsonify({'error': f'Shotstack error {r.status_code}: {r.text}'}), 500
        render_id = r.json()['response']['id']
        return jsonify({'render_id': render_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poll/<render_id>', methods=['GET'])
def poll(render_id):
    shotstack_key = request.args.get('key', '')
    try:
        r = requests.get(
            f'https://api.shotstack.io/stage/render/{render_id}',
            headers={'x-api-key': shotstack_key}
        )
        d = r.json()['response']
        return jsonify({'status': d['status'], 'url': d.get('url', ''), 'error': d.get('error', '')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'  Automaticus running on port {port}')
    app.run(host='0.0.0.0', port=port)
