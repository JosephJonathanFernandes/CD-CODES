Lab Session 7 — YACC/Lex examples

This folder contains multiple small YACC (Bison) + Flex examples for learning syntax and semantic analysis.

Files provided:
- expr.l / expr.y — full expression evaluator (multi-operator expressions, precedence, unary minus) with:
	- floating-point numbers (and integers)
	- variables and simple assignment (name = expr)
	- prefix/postfix ++/-- on identifiers
	- exponentiation (^) and modulo (%)
	- division/modulo by zero reported as errors; no Result printed for that line
- decl.l / decl.y — validate C-like declaration statements (e.g., "int a, b, c;")
- binexpr.l / binexpr.y — strict two-operand expressions: num op num (ints/floats, signs, scientific notation; ops: + - * / % ^)
- assign.l / assign.y — parse and evaluate assignment statements like: x = 3 * (2 + 1); now also supports % and ^ on the RHS

How to build (PowerShell, MinGW/msys or WSL):

# Using bison + flex (Bison produces *.tab.c / *.tab.h)
bison -d <base>.y
flex <base>.l
gcc lex.yy.c <base>.tab.c -o <base>.exe

Examples (run in this folder):

# Full evaluator
bison -d expr.y
flex expr.l
gcc lex.yy.c expr.tab.c -o expr.exe
.\\expr.exe

# Declaration validator
bison -d decl.y
flex decl.l
gcc lex.yy.c decl.tab.c -o decl.exe
.\\decl.exe

# Strict two-operand parser
bison -d binexpr.y
flex binexpr.l
gcc lex.yy.c binexpr.tab.c -o binexpr.exe
.\\binexpr.exe

# Assignment parser
bison -d assign.y
flex assign.l
gcc lex.yy.c assign.tab.c -o assign.exe
.\\assign.exe

Notes:
- On Windows/MinGW you might need to link with -lfl. The lexers here provide a small yywrap() stub so -lfl is not required.
- To quit interactive runs on Windows press Ctrl+Z then Enter.
- If using Bison/Flex from MSYS2 or WSL, commands are the same but run inside those environments.

Running tests (PowerShell):

- Expression evaluator tests
	- Build: `bison -d expr.y; flex expr.l; gcc lex.yy.c expr.tab.c -o expr.exe`
	- Run: `tests\run-expr-tests.ps1`

- Declaration validator tests
	- Build: `bison -d decl.y; flex decl.l; gcc lex.yy.c decl.tab.c -o decl.exe`
	- Run: `tests\run-decl-tests.ps1`

Sample inputs:
- decl:  int a, b, c;
- binexpr: 12 + 5, 12.5 * 2, -3 - -4.5, +1e2 / 4e1, 5 % 2, 2 ^ 3
- expr: 3 + 4 * 5, 1/2, 10.0/4, x = 5, --x, x++, 2^3^2, 5.5 % 2
- assign: x = 3 * (2 + 1); y = 2 ^ 3; z = 5 % 2;

Notes on behavior:
- expr: divides/mods by zero print an error (stderr) and suppress the Result line for that input.
- binexpr: prints "Error: division by zero" or "Error: modulo by zero" and no result for that line.
- assign: on div/mod-by-zero, prints an error and assigns 0 to the variable for that statement.

If you want, I can compile and run any of the examples here and show the outputs, or add small test scripts that run a set of inputs automatically.