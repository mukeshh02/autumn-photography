$workspace = $PSScriptRoot
foreach ($site in @(
    @{Port=3000; Directory=$workspace},
    @{Port=3001; Directory=(Join-Path $workspace 'winter')},
    @{Port=3002; Directory=(Join-Path $workspace 'jessica')},
    @{Port=3003; Directory=(Join-Path $workspace 'liller')},
    @{Port=3004; Directory=(Join-Path $workspace 'solene')}
)) {
    if (-not (Get-NetTCPConnection -State Listen -LocalPort $site.Port -ErrorAction SilentlyContinue)) {
        Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory $site.Directory -WindowStyle Hidden
    }
    Write-Host "http://localhost:$($site.Port)"
}
