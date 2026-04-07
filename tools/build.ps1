# CloudPedagogy Quarto Course Generator - Build Script
# Usage: .\tools\build.ps1 [config_path]

$Config = if ($args[0]) { $args[0] } else { "config/epm102.yml" }

# Ensure we are in the project root
Set-Location "$PSScriptRoot\.."

Write-Host "------------------------------------------------" -ForegroundColor White
Write-Host "🚀 CloudPedagogy Multi-Module Builder" -ForegroundColor Yellow
Write-Host "------------------------------------------------" -ForegroundColor White

Write-Host "Step 1: Validating configuration ($Config)..." -ForegroundColor Cyan
$env:PYTHONPATH = "src"
python3 -m course_generator.cli validate $Config
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Extract module id
$InspectOutput = python3 -m course_generator.cli inspect $Config
$ModuleLine = $InspectOutput | Select-String "Module:"
$ModuleID = ($ModuleLine -split " ")[1].ToLower()

if (-not $ModuleID) {
    Write-Host "Error: Could not identify Module Code from $Config" -ForegroundColor Red
    exit 1
}

$SourceDir = "course\$ModuleID"
$SiteDir = "output\$ModuleID\site"

Write-Host "Step 2: Building Quarto scaffold into '$SourceDir'..." -ForegroundColor Cyan
python3 -m course_generator.cli build $Config --force
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Step 3: Rendering website into '$SiteDir'..." -ForegroundColor Cyan
if (-not (Test-Path "output\$ModuleID")) { New-Item -ItemType Directory -Path "output\$ModuleID" }
quarto render $SourceDir --output-dir "../../output/$ModuleID/site"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "------------------------------------------------" -ForegroundColor White
Write-Host "✅ Done! Module '$ModuleID' is ready." -ForegroundColor Green
Write-Host "Source: $SourceDir" -ForegroundColor White
Write-Host "Website: $SiteDir" -ForegroundColor White
Write-Host "------------------------------------------------" -ForegroundColor White
