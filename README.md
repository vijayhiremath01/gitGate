# 🚀 gitGate

An automated, event-driven **Agentic AI Gateway** that intercepts local Git operations to provide instant, senior-level code reviews before code ever hits your repository. Powered by **Groq** and **Llama 3.3 (70B)**, `gitGate` ensures your commits are structurally sound, secure, and production-ready.

---

## ✨ Features

* **Zero-Latency Infiltration:** Hooks directly into native Git lifecycles (`pre-commit`) to block bugs at the source.
* **Line-by-Line Multi-File Analysis:** Scans multiple files simultaneously and maps vulnerabilities straight to the file name and line number.
* **Intelligent False-Positive Mitigation:** Calibrated with senior engineering lenses that distinguish severe security threats (e.g., exposed API keys) from benign learning/development code (e.g., local print statements, dummy variables).
* **Isolated Environment Execution:** Deploys within a dedicated, hidden virtual environment (`~/.gitgate`) to guarantee zero interference with your system-wide Python dependencies.
* **Interactive Bypass:** Gives the developer immediate `[y/n]` control to force a commit through or drop it gracefully.

---

## 🛠️ Automated 1-Command Installation

You can install `gitGate` into **any local Git repository** instantly by firing this single command in your terminal:

```bash
curl -fsSL [https://gist.githubusercontent.com/vijayhiremath01/345b451dc07198265d43cd20244a8e6e/raw/install.sh](https://gist.githubusercontent.com/vijayhiremath01/345b451dc07198265d43cd20244a8e6e/raw/install.sh) | bash
