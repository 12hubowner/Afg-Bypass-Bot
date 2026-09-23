#!/usr/bin/env python3
"""
Afg Bypass – Web Interface
Rtao API hidden – shows "Afg Bypass"
"""

import os
from flask import Flask, render_template_string, request, jsonify
import requests
import json
import time

app = Flask(__name__)

# ====================================================================
# RTAO API CONFIG (loaded from environment variables)
# ====================================================================
RTAO_API_KEY = os.environ.get("RTAO_API_KEY")
RTAO_API_URL = "https://api.rtao.lol/bypass"

if not RTAO_API_KEY:
    raise SystemExit("ERROR: RTAO_API_KEY environment variable is not set.")

# ====================================================================
# BYPASS ENGINE – RTAO ONLY (HIDDEN)
# ====================================================================
def bypass_rtao(url):
    """Call the Rtao bypass API."""
    try:
        headers = {
            "x-api-key": RTAO_API_KEY,
            "Content-Type": "application/json",
        }
        params = {"url": url}
        response = requests.get(
            RTAO_API_URL, headers=headers, params=params, timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" or data.get("success") is True:
                return data.get("result") or data.get("bypassed") or data.get("url")
            if "result" in data:
                return data["result"]
        return None
    except Exception as e:
        print(f"[Rtao API Error] {e}")
        return None


def getKey(url):
    result = bypass_rtao(url)
    if result:
        return str(result)
    return "bypass fail - Afg Bypass failed"

# ====================================================================
# WEB INTERFACE – FULL DESIGN
# ====================================================================
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Afg Bypass – Link Bypass</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: #0a0a0f;
            overflow-x: hidden;
            position: relative;
        }
        /* AFGHAN FLAG BACKGROUND */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 0;
            background: 
                linear-gradient(0deg, 
                    rgba(0, 0, 0, 0.7) 0%,
                    rgba(0, 0, 0, 0.5) 20%,
                    rgba(0, 0, 0, 0.3) 40%,
                    rgba(0, 0, 0, 0.5) 60%,
                    rgba(0, 0, 0, 0.7) 80%,
                    rgba(0, 0, 0, 0.9) 100%
                ),
                url('https://i.pinimg.com/736x/76/ef/f8/76eff829997dc4df6fbb7c98a4d7fb34.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(2px) saturate(1.2);
            transform: scale(1.05);
        }
        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 0;
            background: radial-gradient(ellipse at center, rgba(10, 10, 15, 0.3) 0%, rgba(10, 10, 15, 0.7) 100%);
            pointer-events: none;
        }
        .glow-neon {
            text-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px #7c3aed, 0 0 80px #7c3aed;
        }
        .btn-neon {
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
            transition: all 0.3s ease;
        }
        .btn-neon:hover {
            box-shadow: 0 0 40px rgba(168, 85, 247, 0.8);
            transform: scale(1.02);
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
            100% { transform: translateY(0px); }
        }
        .float-element {
            animation: float 3.5s ease-in-out infinite;
        }
        .float-delay-1 { animation-delay: 0s; }
        .float-delay-2 { animation-delay: 0.7s; }
        .float-delay-3 { animation-delay: 1.4s; }
        .container {
            max-width: 720px;
            width: 100%;
            background: rgba(18, 18, 26, 0.75);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 40px 32px;
            border: 1px solid rgba(168, 85, 247, 0.3);
            box-shadow: 0 0 60px rgba(168, 85, 247, 0.15), 0 25px 60px rgba(0,0,0,0.8);
            position: relative;
            z-index: 1;
            overflow: hidden;
        }
        .container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at 30% 50%, rgba(168, 85, 247, 0.05) 0%, transparent 60%);
            pointer-events: none;
            animation: float 6s ease-in-out infinite;
        }
        .header {
            text-align: center;
            margin-bottom: 24px;
            position: relative;
            z-index: 1;
        }
        .title {
            font-size: 38px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .title span {
            color: #a855f7;
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.6), 0 0 40px rgba(168, 85, 247, 0.3);
        }
        .subtitle {
            color: #d0d0e0;
            font-size: 15px;
            margin-top: 6px;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
        }

        /* ===== VIDEO GUIDE ===== */
        .video-guide {
            margin: 0 0 24px 0;
            padding: 14px;
            background: rgba(13, 13, 20, 0.6);
            border-radius: 14px;
            border: 1px solid rgba(168, 85, 247, 0.15);
            position: relative;
            z-index: 1;
            text-align: center;
        }
        .video-guide h2 {
            color: #a855f7;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 0.3px;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
        }
        .video-guide .video-wrapper {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 */
            height: 0;
            overflow: hidden;
            border-radius: 10px;
            border: 1px solid #2a2a3a;
            background: #000;
        }
        .video-guide .video-wrapper iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }

        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            position: relative;
            z-index: 1;
        }
        .input-group input {
            flex: 1;
            padding: 16px 20px;
            border-radius: 14px;
            border: 1px solid #2a2a3a;
            background: rgba(13, 13, 20, 0.8);
            color: #e6edf3;
            font-size: 16px;
            outline: none;
            transition: border 0.2s, box-shadow 0.2s;
        }
        .input-group input:focus {
            border-color: #a855f7;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
        }
        .input-group input::placeholder { color: #484f58; }
        .input-group button {
            padding: 16px 32px;
            border-radius: 14px;
            border: none;
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            color: #fff;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.3);
        }
        .input-group button:hover {
            box-shadow: 0 0 50px rgba(168, 85, 247, 0.6);
            transform: scale(1.03);
        }
        .input-group button:active { transform: scale(0.97); }
        .supported {
            display: flex;
            flex-wrap: wrap;
            gap: 10px 16px;
            justify-content: center;
            margin-bottom: 24px;
            padding: 12px;
            background: rgba(13, 13, 20, 0.6);
            border-radius: 12px;
            border: 1px solid rgba(168, 85, 247, 0.15);
            position: relative;
            z-index: 1;
        }
        .supported span {
            color: #c0c0d0;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .supported span::before { content: "✅"; font-size: 14px; }
        .supported span.neon-text {
            color: #a855f7;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
        }
        #result { margin-top: 20px; min-height: 60px; position: relative; z-index: 1; }
        .result-box {
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #2a2a3a;
            background: rgba(13, 13, 20, 0.7);
            animation: fadeIn 0.4s ease;
        }
        .result-box.success {
            border-color: #a855f7;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.15);
        }
        .result-box.fail { border-color: #f85149; }
        .result-box.loading {
            border-color: #d29922;
            box-shadow: 0 0 20px rgba(210, 153, 34, 0.1);
        }
        .result-box .label {
            font-size: 12px;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .result-box .value {
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 14px;
            color: #e6edf3;
            word-break: break-all;
            background: rgba(10, 10, 15, 0.8);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #1a1a2a;
            max-height: 200px;
            overflow-y: auto;
        }
        .result-box .value.success-text {
            color: #a855f7;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
        }
        .result-box .value.fail-text { color: #f85149; }
        .result-box .meta {
            display: flex;
            justify-content: space-between;
            margin-top: 12px;
            font-size: 13px;
            color: #8b949e;
        }
        .result-box .meta a { color: #a855f7; text-decoration: none; }
        .result-box .meta a:hover { text-decoration: underline; }
        .copy-btn {
            margin-top: 12px;
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid #a855f7;
            background: transparent;
            color: #a855f7;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .copy-btn:hover {
            background: #a855f7;
            color: #fff;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
        }
        .footer {
            text-align: center;
            margin-top: 28px;
            font-size: 13px;
            color: #a0a0b0;
            position: relative;
            z-index: 1;
        }
        .footer a {
            color: #a855f7;
            text-decoration: none;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
        }
        .footer a:hover { text-decoration: underline; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #2a2a3a;
            border-top-color: #a855f7;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            vertical-align: middle;
            margin-right: 10px;
        }
        .particle {
            position: fixed;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.15), transparent);
            pointer-events: none;
            z-index: 0;
        }
        .particle-1 { width: 300px; height: 300px; top: -100px; left: -100px; animation: float 5s ease-in-out infinite; }
        .particle-2 { width: 200px; height: 200px; bottom: -50px; right: -50px; animation: float 4s ease-in-out infinite reverse; }
        .particle-3 { width: 150px; height: 150px; top: 40%; right: -60px; animation: float 6s ease-in-out infinite 1s; }
        .particle-4 { width: 100px; height: 100px; bottom: 20%; left: -40px; animation: float 4.5s ease-in-out infinite 0.5s; }

        @media (max-width: 600px) {
            .container { padding: 24px 16px; }
            .input-group { flex-direction: column; }
            .input-group button { width: 100%; }
            .title { font-size: 26px; }
            .video-guide h2 { font-size: 14px; }
            .particle-1, .particle-2, .particle-3, .particle-4 { display: none; }
            body::before { filter: blur(4px) saturate(1.5); }
        }
    </style>
</head>
<body>
    <div class="particle particle-1"></div>
    <div class="particle particle-2"></div>
    <div class="particle particle-3"></div>
    <div class="particle particle-4"></div>

<div class="container">
    <div class="header">
        <div class="title float-element float-delay-2">Afg <span>Bypass</span></div>
        <div class="subtitle float-element float-delay-3">Universal Link Bypass – Plato • Work.ink • Loot • Linkvertise</div>
    </div>

    <!-- ===== VIDEO GUIDE ===== -->
    <div class="video-guide float-element float-delay-1">
        <h2>🎬 How to Bypass a Link – Watch the Guide</h2>
        <div class="video-wrapper">
            <iframe
                src="https://streamable.com/e/26o6m2"
                allowfullscreen
                frameborder="0"
                allow="autoplay; fullscreen"
                title="How to Bypass a Link – Afg Bypass Tutorial">
            </iframe>
        </div>
    </div>

    <div class="supported">
        <span class="neon-text">Plato Relay</span>
        <span>Work.ink</span>
        <span>Linkvertise</span>
        <span>Loot links</span>
        <span class="neon-text">200+ domains</span>
    </div>

    <div class="input-group">
        <input type="text" id="urlInput" placeholder="https://auth.platorelay.com/a?d=..." autofocus>
        <button id="bypassBtn" class="btn-neon">🚀 Bypass</button>
    </div>

    <div id="result"></div>

    <div class="footer">
        Afg Bypass Web • v1.2.0 • <span id="date"></span>
        <br>
        <a href="https://discord.gg/ht9Jhn2n8P" target="_blank">💜 Support Server</a>
    </div>
</div>

<script>
    document.getElementById('date').textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });

    const input = document.getElementById('urlInput');
    const btn = document.getElementById('bypassBtn');
    const resultDiv = document.getElementById('result');

    async function bypass() {
        const url = input.value.trim();
        if (!url) {
            resultDiv.innerHTML = `<div class="result-box fail"><div class="label">⚠️ Error</div><div class="value fail-text">Please enter a valid URL.</div></div>`;
            return;
        }

        resultDiv.innerHTML = `<div class="result-box loading"><div class="label">⏳ Processing</div><div class="value"><span class="spinner"></span> Bypassing with Afg Bypass...</div></div>`;

        try {
            const res = await fetch('/bypass', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });
            const data = await res.json();

            if (data.success) {
                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <div class="label">✅ Afg Bypass Success</div>
                        <div class="value success-text">${escapeHtml(data.result)}</div>
                        <div style="margin-top:10px;">
                            <button class="copy-btn" onclick="copyResult('${escapeHtml(data.result)}')">📋 Copy Result</button>
                        </div>
                        <div class="meta">
                            <span>⏱️ ${data.time || 'N/A'}</span>
                            <span><a href="${escapeHtml(url)}" target="_blank">🔗 Original Link</a></span>
                        </div>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <div class="result-box fail">
                        <div class="label">❌ Afg Bypass Failed</div>
                        <div class="value fail-text">${escapeHtml(data.result || 'Unknown error')}</div>
                        <div class="meta">
                            <span>🔗 <a href="${escapeHtml(url)}" target="_blank">Original Link</a></span>
                        </div>
                    </div>
                `;
            }
        } catch (err) {
            resultDiv.innerHTML = `<div class="result-box fail"><div class="label">❌ Error</div><div class="value fail-text">${escapeHtml(err.message)}</div></div>`;
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function copyResult(text) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.querySelector('.copy-btn');
            if (!btn) return;
            const orig = btn.textContent;
            btn.textContent = '✅ Copied!';
            setTimeout(() => btn.textContent = orig, 2000);
        }).catch(() => {
            alert('Copy failed. Select and copy manually.');
        });
    }

    btn.addEventListener('click', bypass);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') bypass(); });
    input.focus();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/bypass', methods=['POST'])
def bypass():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'success': False, 'result': 'No URL provided'})

    start = time.time()
    result = getKey(url)
    elapsed = round(time.time() - start, 2)

    if result and not result.startswith('bypass fail'):
        return jsonify({'success': True, 'result': result, 'time': f'{elapsed}s'})
    return jsonify({'success': False, 'result': result, 'time': f'{elapsed}s'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"""
    ╔═══════════════════════════════════════╗
    ║   🇦🇫  AFG BYPASS WEB  🇦🇫           ║
    ║   Afghan Flag + Neon Purple          ║
    ║   API: Rtao.lol                      ║
    ║   http://localhost:{port}              ║
    ╚═══════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False)
