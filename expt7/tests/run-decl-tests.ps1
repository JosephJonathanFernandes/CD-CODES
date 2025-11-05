# Runs decl.exe against all test inputs in tests/decl and compares stdout to *.actual
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root 'decl.exe'
$declDir = Join-Path $PSScriptRoot 'decl'

if (-not (Test-Path $exe)) {
  Write-Host "decl.exe not found at $exe. Build it first (see README.md)." -ForegroundColor Yellow
  exit 1
}

$tests = Get-ChildItem -Path $declDir -Filter *.in | Sort-Object Name
if (-not $tests) {
  Write-Host "No decl tests found in $declDir" -ForegroundColor Yellow
  exit 1
}

$pass = 0
$fail = 0
foreach ($t in $tests) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($t.Name)
  $actualPath = Join-Path $t.DirectoryName ($name + '.actual')
  $outPath = Join-Path $t.DirectoryName ($name + '.out')

  if (-not (Test-Path $actualPath)) {
    Write-Host "Missing expected file: $actualPath" -ForegroundColor Red
    $fail++
    continue
  }

  # Pipe the single declaration line to decl.exe, ignore stderr, capture stdout
  Get-Content $t.FullName | & $exe 2>$null | Out-File -Encoding ascii $outPath

  $diff = Compare-Object (Get-Content $actualPath) (Get-Content $outPath)
  if ($diff) {
    Write-Host ("FAIL: {0}" -f $name) -ForegroundColor Red
    $fail++
  } else {
    Write-Host ("PASS: {0}" -f $name) -ForegroundColor Green
    $pass++
  }
}

Write-Host ("Total: {0}  Passed: {1}  Failed: {2}" -f $tests.Count, $pass, $fail)
if ($fail -eq 0) { exit 0 } else { exit 1 }
