$workspace = $PSScriptRoot
foreach ($site in @(@{Port=3000; Directory=$workspace}, @{Port=3001; Directory=(Join-Path $workspace 'winter')})) {
    $listener = Get-NetTCPConnection -State Listen -LocalPort $site.Port -ErrorAction SilentlyContinue
    if (-not $listener) {
        Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory $site.Directory -WindowStyle Hidden
        Write-Host "Started website on http://localhost:$($site.Port)"
    } else {
        Write-Host "Port $($site.Port) already has a running server."
    }
}
