expt6 - Predictive parser helper

Overview

This small Python utility loads a grammar from a text file, applies standard
transformations (indirect/direct left-recursion removal and left-factoring),
computes FIRST and FOLLOW sets, builds a predictive (LL(1)) parsing table,
and runs a table-driven predictive parser while printing detailed, step-by-step
trace information useful for learning or assignments.

What it prints

- Original grammar (as read from the grammar file)
- Step-by-step left-recursion elimination (indirect & direct) with the exact
  replacements performed
- Step-by-step left-factoring actions
- Grammar after each transformation
- FIRST sets and FOLLOW sets (formatted)
- Generated parsing table (grid)
- LL(1) conflict report (if any table cells are filled by multiple productions)
- Detailed parse trace (Buffer | Stack | Action) showing table lookups and stack
  updates; epsilon is printed as 'ε'.

Grammar file format

- Plain UTF-8 text.
- Comments: lines starting with `#` are ignored.
- Optional start symbol: `Start: S` (if omitted the first LHS is used)
- Optional input string: `Input: a b c` (if omitted you can pass `--input-string`)
- Productions use `->` in the file. Example:

  S -> A k O
  A -> A d | a B | a C
  B -> b B C | r
  C -> c

Notes:
- Use spaces between symbols in RHS alternatives. Use `ε` or `eps` for epsilon.

Quick usage (PowerShell on Windows)

- Run the parser on the default `grammar.txt`:

```powershell
python expt6.py
```

- Run with a specific grammar file:

```powershell
python expt6.py --grammar tests/grammars/factor_example.txt
```

- Provide an inline input string (tokens space-separated where needed):

```powershell
python expt6.py --grammar tests/grammars/factor_example.txt --input-string "a r k O"
```

Test suite

A small test harness is included under `tests/`.

- Grammar examples: `tests/grammars/*.txt`
- Runner: `tests/run_tests.py` — runs `expt6.py` on each grammar and saves full
  outputs to `tests/results/`.

Run all tests:

```powershell
python tests\run_tests.py
```

Configuration and small tweaks

- Printed production arrow: the program prints productions using the
  `PROD_ARROW` symbol defined near the top of `expt6.py` (default: '⇒').
  This is only a display choice — the grammar file syntax still requires
  `->`. Change `PROD_ARROW` in `expt6.py` if you want a different symbol
  (e.g. `=>` or `->`).

- Epsilon: printed as `ε` in outputs. The code handles `ε` and `eps` in
  grammar files.

Internals / Notes for instructors

- FIRST sets are computed with an iterative fixpoint algorithm.
- FOLLOW sets are computed iteratively as well.
- Table construction records the production which populated each cell and
  reports conflicts (so you can see "existing" vs "new" production for a
  conflicting T[A][t]).
- The parser trace prints stack with the stack-top on the left (textual
  convention matching many textbooks) and prints the updated stack after
  expanding a non-terminal.

Next improvements you may want

- Add command-line flags to control verbosity (e.g., `--no-transform`,
  `--no-trace`) or to choose a production arrow symbol at runtime.
- Add an `Expect:` field to grammar files so tests can assert PASS/FAIL.
- Export results as Markdown/HTML for assignment submission.

License

Use or modify for your classwork. No warranty.
