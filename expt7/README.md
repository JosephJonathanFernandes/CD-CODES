Lab Session 7 — YACC/Lex examples

This folder contains multiple small YACC (Bison) + Flex examples for learning syntax and semantic analysis.

Files provided:
- expr.l / expr.y — full expression evaluator (supports multi-operator expressions, precedence, unary minus)
- decl.l / decl.y — validate C-like declaration statements (e.g., "int a, b, c;")
- binexpr.l / binexpr.y — strict two-operand expressions in form: num1 op num2
- assign.l / assign.y — parse and evaluate assignment statements like: x = 3 * (2 + 1);

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

Sample inputs:
- decl:  int a, b, c;
- binexpr: 12 + 5
- expr: 3 + 4 * 5
- assign: x = 3 * (2 + 1);

If you want, I can compile and run any of the examples here and show the outputs, or add small test scripts that run a set of inputs automatically.