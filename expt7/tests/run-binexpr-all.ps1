# Runs binexpr.exe against a single consolidated test file (tests/binexpr/all.tst)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root 'binexpr.exe'
$dir = Join-Path $PSScriptRoot 'binexpr'
$inputFile = Join-Path $dir 'all.tst'
$expectedFile = Join-Path $dir 'all.actual'
$outFile = Join-Path $dir 'all.out'

if (-not (Test-Path $exe)) {
  Write-Host "binexpr.exe not found at $exe. Build it first (see README.md)." -ForegroundColor Yellow
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

# Run binexpr.exe as a single session, ignoring stderr, capturing stdout
Get-Content $inputFile | & $exe 2>$null | Out-File -Encoding ascii $outFile

# Compare expected vs actual
$diff = Compare-Object (Get-Content $expectedFile) (Get-Content $outFile)
if ($diff) {
  Write-Host "FAIL: differences found between all.actual and all.out" -ForegroundColor Red
  Write-Host "Use a diff tool to compare:`n  $expectedFile`n  $outFile" -ForegroundColor Yellow
  exit 1
} else {
  Write-Host "PASS: consolidated binexpr tests" -ForegroundColor Green
  exit 0
}
