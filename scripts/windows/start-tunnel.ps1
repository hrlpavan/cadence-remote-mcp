<#
.SYNOPSIS
    Automated script to start Cloudflare Quick Tunnel on Windows.
#>

param(
    [int]$Port = 8090
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "       Cadence-Remote-MCP: Cloudflare Quick Tunnel        " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$cloudflared = (Get-ChildItem -Path "C:\Program Files*", "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "cloudflared.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName

if (-not $cloudflared) {
    Write-Host "[*] cloudflared not found. Installing via winget..." -ForegroundColor Yellow
    winget install Cloudflare.cloudflared --accept-package-agreements --accept-source-agreements
    $cloudflared = (Get-ChildItem -Path "C:\Program Files*", "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "cloudflared.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
}

Write-Host "[+] Starting tunnel to http://127.0.0.1:$Port..." -ForegroundColor Green
Write-Host "[!] Copy the https://xxxx.trycloudflare.com URL and add it to your Mac MCP config." -ForegroundColor Magenta

& "$cloudflared" tunnel --url "http://127.0.0.1:$Port"
