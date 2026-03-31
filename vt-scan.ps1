# VT TUI Scanner — Script PowerShell pour usage quotidien
# Usage: .\vt-scan.ps1 -File C:\path\to\file.exe

param(
    [Parameter(Mandatory=$false)]
    [string]$File,
    
    [Parameter(Mandatory=$false)]
    [string]$Url,
    
    [Parameter(Mandatory=$false)]
    [string]$Dir,
    
    [Parameter(Mandatory=$false)]
    [switch]$Export
)

# Activer l'environnement virtuel si nécessaire
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
}

# Exécuter le scanner
if ($File) {
    Write-Host "🔍 Scan du fichier : $File" -ForegroundColor Cyan
    python -m src.main --headless --file $File --verbose
    if ($Export) { python -m src.main --headless --file $File --export json }
}
elseif ($Url) {
    Write-Host "🔍 Scan de l'URL : $Url" -ForegroundColor Cyan
    python -m src.main --headless --url $Url --verbose
}
elseif ($Dir) {
    Write-Host "🔍 Scan du dossier : $Dir" -ForegroundColor Cyan
    python -m src.main --headless --dir $Dir --verbose
    if ($Export) { python -m src.main --headless --dir $Dir --export csv }
}
else {
    Write-Host "VT TUI Scanner — Usage :" -ForegroundColor Yellow
    Write-Host "  .\vt-scan.ps1 -File C:\path\file.exe" -ForegroundColor Gray
    Write-Host "  .\vt-scan.ps1 -Url https://example.com" -ForegroundColor Gray
    Write-Host "  .\vt-scan.ps1 -Dir C:\Downloads" -ForegroundColor Gray
    Write-Host "  .\vt-scan.ps1 -File C:\file.exe -Export" -ForegroundColor Gray
}
