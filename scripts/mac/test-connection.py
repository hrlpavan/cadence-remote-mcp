#!/usr/bin/env python3
"""
Test script to verify connectivity from macOS to the Windows Cadence MCP Worker Node.
"""

import sys
import json
import urllib.request

def test_connection(url: str, auth_key: str):
    print(f"[*] Testing connection to: {url}")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {auth_key}"
    }

    # 1. Initialize
    init_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "macbook-client", "version": "1.0"}
        }
    }).encode()

    req = urllib.request.Request(url, data=init_payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            session_id = resp.headers.get("mcp-session-id")
            raw = resp.read().decode()
            print("[+] Successfully initialized MCP Session!")
            print(f"[+] Session ID: {session_id}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return False

    headers["mcp-session-id"] = session_id

    # 2. List tools
    tools_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }).encode()

    req = urllib.request.Request(url, data=tools_payload, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode()
        for line in raw.splitlines():
            if line.startswith("data: "):
                d = json.loads(line[6:])
                tools = d.get("result", {}).get("tools", [])
                print(f"[+] Total Tools Available on Windows Node: {len(tools)}")
                print("[+] Key Execution Tools:")
                for t in tools:
                    if t["name"] in ["Shell", "App", "Snapshot", "FileRead", "FileWrite"]:
                        print(f"    - {t['name']}: {t.get('description', '')[:60]}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test-connection.py <URL> [AUTH_KEY]")
        print("Example: python3 test-connection.py https://xxxx.trycloudflare.com/mcp cadence-mcp-key")
        sys.exit(1)

    endpoint = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else "cadence-mcp-key"
    test_connection(endpoint, key)
