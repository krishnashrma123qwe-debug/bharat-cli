# ⚡ BharatCLI — Terminal AI Pair Programmer & Code Review Agent

> **Powered by BharatCode Qwen 3.8 27B (256k Context Window)**  
> Built for the **BharatCode Build League 2026** • Category: *Coding & Developer Tools*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Model: Qwen 3.8 27B](https://img.shields.io/badge/Model-BharatCode%20Qwen%203.8%2027B-orange.svg)](https://bharatcode.ai)
[![Author: Krishna Sharma](https://img.shields.io/badge/Author-Krishna%20Sharma-cyan.svg)](https://github.com/krishnashrma123qwe-debug)

---

## 🎯 The Mission
Developers lose hours context-switching between the terminal, browser tabs, and bloated AI web interfaces just to diagnose an error or review a pull request.

**BharatCLI** brings sovereign, Indian-priced AI intelligence directly into your shell. Powered by BharatCode's **Qwen 3.8 27B** inference gateway, it provides:
* **Zero Context Switching:** Instant AI diagnostics without leaving your terminal.
* **Automated Code Review:** Scans files for critical security vulnerabilities, performance anti-patterns, and code smells.
* **Smart Traceback Explainer:** Parses terminal errors and generates exact, copy-pasteable patches.
* **Dual Interface (CLI + Local Web Workbench):** Run `bharat ui` to launch an instant local visual code studio.

---

## 🚀 Quickstart & Installation

### 1. Clone & Install
```bash
git clone https://github.com/krishnashrma123qwe-debug/bharat-cli.git
cd bharat-cli
pip install -r requirements.txt
pip install -e .
```

### 2. Configure Your BharatCode API Key
```bash
bharat auth --key bc_live_your_api_key_here
```
*(Your key is securely persisted to `~/.bharatcode/config.json`)*

### 3. Verify Connection
```bash
bharat status
```

---

## 💻 Commands & Workflow

### 1. Automated Code Review
Audit any source file for bugs, SQL injections, and performance bottlenecks:
```bash
bharat review examples/bug_sample.py
```
To run a strict security-only audit:
```bash
bharat review app/auth.py --security-only
```

### 2. Traceback & Error Explainer
Diagnose crash logs or pipe terminal stderr directly into BharatCLI:
```bash
# Pass error log file
bharat explain examples/error_log.txt

# Or pipe output directly from failed command
python broken_script.py 2>&1 | bharat explain
```

### 3. Code Generation
Generate clean, production-ready code with type annotations:
```bash
bharat gen "FastAPI middleware for rate limiting using Redis" -o rate_limit.py
```

### 4. BharatCode Studio (Local Web Workbench)
Launch an interactive visual code playground on `http://127.0.0.1:8484`:
```bash
bharat ui
```

---

## 🏗️ Architecture

```
bharat-cli/
├── BharatCode.txt                   # Hackathon verification token
├── bharat/
│   ├── cli.py                       # Click CLI command dispatcher
│   ├── client.py                    # BharatCode API wrapper (Qwen 3.8 27B)
│   ├── ui.py                        # Rich terminal formatting & syntax engine
│   └── web_server.py                # Local web studio workbench (Port 8484)
├── examples/
│   ├── bug_sample.py                # Test files for review evaluation
│   └── error_log.txt                # Sample crash tracebacks
├── setup.py                         # Standard Python package installer
└── README.md
```

---

## 🛡️ Hackathon Verification & Compliance
* **Repository Root Token:** Verified via [`BharatCode.txt`](BharatCode.txt)
* **Model Inference:** Configured for `qwen-3.8-27b` via `https://bharatcode.ai/api/model/v1`
* **Author:** Krishna Sharma ([@krishnashrma123qwe-debug](https://github.com/krishnashrma123qwe-debug))
* **License:** MIT License
