import http.server
import socketserver
import webbrowser
import threading
import json
import urllib.parse
from bharat.client import BharatCodeClient

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BharatCode AI Studio | Local Workbench</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #080C14; color: #F1F5F9; }
    .mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="p-6 max-w-6xl mx-auto">
  <header class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-orange-500 flex items-center justify-center font-black text-white text-lg">B</div>
      <div>
        <h1 class="text-xl font-bold tracking-tight">Bharat<span class="text-orange-400">Code</span> Studio</h1>
        <p class="text-xs text-slate-400 font-mono">Powered by Qwen 3.8 27B Inference API</p>
      </div>
    </div>
    <div class="flex items-center gap-2 text-xs font-mono">
      <span class="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">● Local Harness Active</span>
      <span class="px-2.5 py-1 rounded bg-slate-800 text-slate-300">Port 8484</span>
    </div>
  </header>

  <main class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-4">
      <div class="flex items-center justify-between">
        <label class="text-xs font-bold uppercase tracking-wider text-slate-400">Input Code / Stack Trace</label>
        <select id="actionType" class="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-cyan-400">
          <option value="review">Automated Code Review</option>
          <option value="explain">Diagnose Error / Traceback</option>
          <option value="refactor">Performance Refactor</option>
          <option value="tests">Generate Unit Tests</option>
        </select>
      </div>
      <textarea id="codeInput" rows="16" placeholder="// Paste Python, JS, C++, or terminal error log here..."
        class="w-full bg-[#050811] border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400 resize-none"></textarea>
      
      <button onclick="runAnalysis()" id="analyzeBtn" class="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-600 to-orange-500 text-white font-bold text-xs uppercase tracking-wider hover:opacity-90 transition-all flex items-center justify-center gap-2">
        <span>Run BharatCode Analysis</span>
      </button>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <span class="text-xs font-bold uppercase tracking-wider text-cyan-400">AI Output & Recommendations</span>
          <span id="statusBadge" class="text-[11px] font-mono text-slate-400">Ready</span>
        </div>
        <div id="outputArea" class="bg-[#050811] border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 min-h-[380px] overflow-auto whitespace-pre-wrap leading-relaxed">
Click "Run BharatCode Analysis" to test the AI coding harness.
        </div>
      </div>
      <div class="pt-4 border-t border-slate-800 text-center text-xs text-slate-500 font-mono">
        BharatCode Build League 2026 • Author: Krishna Sharma
      </div>
    </div>
  </main>

  <script>
    async function runAnalysis() {
      const code = document.getElementById('codeInput').value.trim();
      const action = document.getElementById('actionType').value;
      if (!code) {
        alert('Please paste some code or error log first!');
        return;
      }

      const btn = document.getElementById('analyzeBtn');
      const out = document.getElementById('outputArea');
      const status = document.getElementById('statusBadge');

      btn.disabled = true;
      btn.innerText = 'Analyzing with Qwen 3.8 27B...';
      status.innerText = '● Processing...';
      status.className = 'text-[11px] font-mono text-amber-400 animate-pulse';

      try {
        const resp = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: code, action: action })
        });
        const data = await resp.json();
        out.innerText = data.result || 'No response returned.';
        status.innerText = '✓ Completed';
        status.className = 'text-[11px] font-mono text-emerald-400';
      } catch (err) {
        out.innerText = 'Error connecting to local server: ' + err;
        status.innerText = '✘ Error';
        status.className = 'text-[11px] font-mono text-red-400';
      } finally {
        btn.disabled = false;
        btn.innerText = 'Run BharatCode Analysis';
      }
    }
  </script>
</body>
</html>
"""

class StudioRequestHandler(http.server.SimpleHTTPRequestHandler):
    client = None

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            code = data.get("code", "")
            action = data.get("action", "review")

            prompts = {
                "review": f"Perform a comprehensive code review of the following snippet. Highlight security flaws, performance optimizations, and provide clean refactored code:\n\n{code}",
                "explain": f"Analyze this error traceback or bug report. Explain the root cause clearly and provide the exact patch to fix it:\n\n{code}",
                "refactor": f"Refactor this code for optimal execution speed, modularity, and modern Python best practices:\n\n{code}",
                "tests": f"Generate thorough unit tests using pytest for this code:\n\n{code}"
            }

            system_prompt = "You are BharatCode AI, an expert software engineer powered by Qwen 3.8 27B."
            prompt = prompts.get(action, prompts["review"])

            try:
                res = self.client.generate(prompt=prompt, system=system_prompt)
            except Exception as e:
                res = f"Inference Notice: {e}"

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"result": res}).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

def start_web_studio(port: int = 8484):
    """Start local Studio UI."""
    client = BharatCodeClient()
    StudioRequestHandler.client = client
    
    server = socketserver.TCPServer(("127.0.0.1", port), StudioRequestHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"\n🚀 BharatCode Studio running at: {url}")
    webbrowser.open(url)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping BharatCode Studio...")
        server.server_close()
