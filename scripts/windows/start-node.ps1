<#
.SYNOPSIS
    Automated startup script for Cadence Remote MCP Worker Node on Windows.
#>

param(
    [string]$HostAddress = "0.0.0.0",
    [int]$Port = 8090,
    [string]$AuthKey = "cadence-mcp-key"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Cadence-Remote-MCP: Windows Execution Worker Node      " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Locate or install Python
$pythonPath = (Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python", "C:\Program Files\Python*" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName

if (-not $pythonPath) {
    Write-Host "[*] Python not found. Installing Python 3.12 via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $pythonPath = (Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python", "C:\Program Files\Python*" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
}

Write-Host "[+] Using Python at: $pythonPath" -ForegroundColor Green

# 2. Check and install winremote-mcp
Write-Host "[*] Checking winremote-mcp installation..." -ForegroundColor Yellow
& "$pythonPath" -m pip install --upgrade winremote-mcp

# 3. Configure Windows Firewall
Write-Host "[*] Ensuring Windows Firewall allows port $Port..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "Cadence Remote MCP ($Port)" -Direction Inbound -LocalPort $Port -Protocol TCP -Action Allow -Profile Any -ErrorAction SilentlyContinue | Out-Null

# 4. Start Server
Write-Host "[+] Starting winremote-mcp on ${HostAddress}:${Port}..." -ForegroundColor Green
Write-Host "[!] Leave this window open. Press CTRL+C to stop." -ForegroundColor Magenta
& "$pythonPath" -m winremote --host $HostAddress --port $Port --enable-all --auth-key $AuthKey
