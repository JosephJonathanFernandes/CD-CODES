import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
GRAM_DIR = ROOT / 'grammars'
RESULT_DIR = ROOT / 'results'
RESULT_DIR.mkdir(exist_ok=True)

files = sorted(GRAM_DIR.glob('*.txt'))
if not files:
    print('No grammar files found in', GRAM_DIR)
    sys.exit(1)

summary = []
for g in files:
    name = g.stem
    out_file = RESULT_DIR / (name + '.out')
    print('Running test:', name)
    cmd = [sys.executable, str(Path(__file__).parent.parent / 'expt6.py'), '--grammar', str(g)]
    try:
        env = dict(**subprocess.os.environ)
        env['PYTHONIOENCODING'] = 'utf-8'
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=10, env=env)
        output = proc.stdout + '\n' + proc.stderr
    except subprocess.TimeoutExpired:
        output = 'TIMEOUT'

    out_file.write_text(output, encoding='utf-8')
    # extract parse result if present
    if 'Parse result:' in output:
        # find the last occurrence
        for line in reversed(output.splitlines()):
            if 'Parse result:' in line:
                parse_res = line.split('Parse result:')[-1].strip()
                break
    else:
        parse_res = 'Unknown'
    summary.append((name, parse_res))

print('\nSummary:')
for name, parse_res in summary:
    print(f"- {name}: {parse_res}")

print('\nDetailed outputs are saved in', RESULT_DIR)
