# ⚡ Cadence-Remote-MCP: Prompt on Mac, Execute on Windows

> **Distributed AI Agent Infrastructure for Cadence Allegro X, OrCAD, and Heavy EDA Workloads via Model Context Protocol (MCP)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue.svg)](https://modelcontextprotocol.io)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%2011-success.svg)]()
[![EDA](https://img.shields.io/badge/EDA-Cadence%20Allegro%20X-red.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)]()

---

## 💡 The Problem & The Solution

Designing multi-layer printed circuit boards (PCBs) in enterprise hardware suites like **Cadence Allegro X** requires massive system resources: 50+ GB of disk space, dedicated NVIDIA GPUs, and 32–64 GB of RAM.

For engineers daily-driving portable setups like a **MacBook Air (M1/M2/M3)**:
- ❌ **Local Virtualization (Parallels/VMware)** divides limited unified memory, degrades battery, and consumes 120+ GB of local SSD space.
- ❌ **Native Windows Dual Boot** is impossible on Apple Silicon.

**Cadence-Remote-MCP solves this completely** by decoupling the **Orchestration Layer** from the **Execution Layer**:
- **Prompt on macOS**: Use Google Antigravity, Claude Desktop, or Cursor on your lightweight Mac.
- **Execute on Windows**: The physical workload runs on an external high-spec Windows workstation (Intel Core i9/i5 HX, RTX GPU, 32GB+ RAM) via remote MCP over secure HTTP/SSE.

---

## 🏛️ System Architecture

```
+───────────────────────────────────+                    +─────────────────────────────────────────+
│       MacBook Air (Client)        │                    │       Windows Workstation (Node)        │
├───────────────────────────────────┤                    ├─────────────────────────────────────────┤
│  [Google Antigravity / Cursor]    │   Remote HTTP      │   [winremote-mcp Server v4.1+]          │
│                │                  │   (SSE / JSON-RPC) │                 │                       │
│                ▼                  │                    │                 ▼                       │
│    Natural Language Prompts       ├───────────────────►│    Native PowerShell Shell Tools        │
│   "Route layer 3, print HRL..."   │  (Tunnel / LAN)    │    Cadence Allegro X CLI / SKILL Engine │
│                ▲                  │                    │    Real-Time Display / GPU Pipelines    │
│                │                  │                    │                 │                       │
│   Receives Live Screen & Logs     │◄───────────────────┤    Captured Window & DRC Telemetry      │
+───────────────────────────────────+                    +─────────────────────────────────────────+
```

---

## ✨ Key Features

- **Decoupled Architecture**: Prompt on macOS with zero fan noise; execute heavy Cadence calculations on a remote Windows workstation.
- **Full Tier 1–3 MCP Tooling (45+ Tools)**:
  - `Shell`: Execute PowerShell, batch scripts, and Cadence CLI (`allegro`, `extracta`, `dbdoctor`, `tclsh`).
  - `App`: Launch, focus, resize, and close Cadence Allegro X, OrCAD X, and System Capture.
  - `Snapshot` & `AnnotatedSnapshot`: Live visual feedback of the active PCB canvas streamed directly to your AI agent.
  - `FileRead` / `FileWrite` / `FileUpload` / `FileDownload`: Seamless two-way transfer of `.brd`, `.dsn`, gerbers, and SKILL scripts.
- **Zero-Config Network Traversal**:
  - Works over local Wi-Fi / Ethernet LAN.
  - Works over **Cloudflare Quick Tunnels** or **Tailscale** to effortlessly bypass strict router AP/Client Isolation (ideal for universities, offices, and coffee shops).
- **Hardened Security**: Protected with Bearer token authentication and isolated workspace drives (`D:\CadenceProjects`).

---

## 🏭 Industry & Enterprise Applications

1. **Hardware & Semiconductor Startups**:
   - Engineers can carry portable MacBooks for mobility while pooling expensive on-premise Windows workstation towers with dedicated licenses.
2. **Autonomous PCB Agent Pipelines**:
   - Integrate LLMs to inspect board layouts, run automated Design Rule Checks (DRC), and verify trace clearances programmatically via continuous agent loops.
3. **University Engineering Labs**:
   - Students can connect to shared department lab workstations without needing to install 60 GB EDA packages or configure complex VPNs.
4. **CI/CD Hardware Verification**:
   - Trigger remote board generation, layer Gerber exports, and impedance simulation checks as automated GitHub Actions / GitLab CI worker steps.

---

## 🚀 Quickstart Guide

### Step 1: Set Up the Windows Workstation (Execution Node)

1. Open **PowerShell** on your Windows workstation.
2. Clone or run our automated setup script:
   ```powershell
   # Install winremote-mcp
   python -m pip install winremote-mcp

   # Start the MCP server with authentication & full tool tier execution
   python -m winremote --host 0.0.0.0 --port 8090 --enable-all --auth-key "cadence-mcp-key"
   ```

3. **Expose the Endpoint** (If your local router blocks device-to-device Wi-Fi traffic):
   ```powershell
   # Run automated Cloudflare quick tunnel (0 accounts needed)
   winget install Cloudflare.cloudflared
   cloudflared tunnel --url http://127.0.0.1:8090
   ```
   *Note the generated public URL (e.g. `https://xxxx.trycloudflare.com`).*

---

### Step 2: Configure the Client (MacBook Air / Orchestrator)

Add the server to your agent MCP configuration:

#### For Google Antigravity (`~/.gemini/config/mcp_config.json`):
```json
{
  "mcpServers": {
    "cadence-worker": {
      "serverUrl": "https://xxxx.trycloudflare.com/mcp",
      "headers": {
        "Authorization": "Bearer cadence-mcp-key"
      }
    }
  }
}
```

#### For Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "cadence-worker": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://xxxx.trycloudflare.com/mcp",
        "--header",
        "Authorization: Bearer cadence-mcp-key"
      ]
    }
  }
}
```

---

## 🧪 Proof of Concept: The "HRL" Test Board

We validated the pipeline end-to-end by prompting from macOS to:
1. Initialize the remote session on a Windows 11 machine (`Intel Core i5-14450HX`).
2. Generate an isolated project directory (`D:\CadenceProjects\HRL_Test\`).
3. Synthesize a 2-layer FR-4 PCB layout with **`HRL`** silkscreen text and test headers.
4. Launch the preview in real-time on the Windows screen and stream a live camera snapshot back to macOS.

---

## 👥 Contributors

This open-source project was created and engineered by:

- **[Pavan Kumar Sadashiv](https://github.com/hrlpavan)** — *Backend, AI Agent Systems & Infrastructure*
- **[Sugam](https://github.com)** — *Hardware & EDA Workflows Co-Creator*

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
