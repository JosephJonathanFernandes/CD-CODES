# Runs expr.exe against all test inputs in tests/expr and compares stdout to *.actual
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root 'expr.exe'
$exprDir = Join-Path $PSScriptRoot 'expr'

if (-not (Test-Path $exe)) {
  Write-Host "expr.exe not found at $exe. Build it first (see README.md)." -ForegroundColor Yellow
  exit 1
}

$tests = Get-ChildItem -Path $exprDir -Filter *.in | Sort-Object Name
if (-not $tests) {
  Write-Host "No expr tests found in $exprDir" -ForegroundColor Yellow
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

  # Run test: pipe input to expr.exe, ignore stderr, capture stdout
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
