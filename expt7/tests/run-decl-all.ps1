# Runs decl.exe against a single consolidated test file (tests/decl/all.tst)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root 'decl.exe'
$declDir = Join-Path $PSScriptRoot 'decl'
$inputFile = Join-Path $declDir 'all.tst'
$expectedFile = Join-Path $declDir 'all.actual'
$outFile = Join-Path $declDir 'all.out'

if (-not (Test-Path $exe)) {
  Write-Host "decl.exe not found at $exe. Build it first (see README.md)." -ForegroundColor Yellow
  exit 1
}

if (-not (Test-Path $inputFile)) {
  Write-Host "Input file not found: $inputFile" -ForegroundColor Red
  exit 1
}

if (-not (Test-Path $expectedFile)) {
  Write-Host "Expected file not found: $expectedFile" -ForegroundColor Red
  exit 1
}

# Remove previous output if any
if (Test-Path $outFile) { Remove-Item $outFile }

# Run decl.exe once per line to honor the single-declaration parser
Get-Content $inputFile | ForEach-Object {
  $_ | & $exe 2>$null | Add-Content -Encoding ascii $outFile
}

# Compare expected vs actual
$diff = Compare-Object (Get-Content $expectedFile) (Get-Content $outFile)
if ($diff) {
  Write-Host "FAIL: differences found between all.actual and all.out" -ForegroundColor Red
  Write-Host "Use a diff tool to compare:`n  $expectedFile`n  $outFile" -ForegroundColor Yellow
  exit 1
} else {
  Write-Host "PASS: consolidated decl tests" -ForegroundColor Green
  exit 0
}
