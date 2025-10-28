YACC/Flex: Validation of basic and nested for/while/do-while loops

Files provided
- for.y         — Bison/YACC grammar (parser)
- for.l         — Flex/Lex scanner (tokenizer)
- sample_inputs.txt — Example inputs (valid and invalid)

Goal
Validate syntax of basic and nested for-loops, while-loops, and do-while loops with assignment statements.
This version also supports simple declarations (e.g. `int x;`, `int y = 2;`) and improved expression parsing with operator precedence (*/ before +- and parentheses), plus unary minus.

How it works (contract)
- Input: a C-like snippet containing assignment statements, for-loops and blocks.
- Output: prints either "Input is syntactically correct." or "Input has syntax errors." and the parser will print syntax error location using line numbers.
- Error modes: syntax errors are reported via yyerror with the line number.

Building and running (Windows notes)

Prerequisites (one of the options):
- Install Win flex-bison (https://github.com/westes/flex/tree/master) and a GCC toolchain like MinGW or MSYS2.
- Or use WSL (Windows Subsystem for Linux) with flex and bison installed.

Recommended steps (PowerShell; adapt if using WSL):

1) Using GNU tools (winflexbison / mingw) installed and on PATH
   cd "c:\Users\Joseph\Desktop\compiler design\expt8"
   bison -d -v for.y           # generates for.tab.c and for.tab.h
   flex for.l                  # generates lex.yy.c
   gcc -o forparser for.tab.c lex.yy.c -lfl   # may need -lfl or libflex on Windows

2) Using WSL (Ubuntu) — open WSL shell and run inside project folder
   bison -d for.y
   flex for.l
   gcc -o forparser for.tab.c lex.yy.c -lfl

Run
- Then feed a source:
  cat sample_inputs.txt | ./forparser
  # or on Windows PowerShell
  Get-Content sample_inputs.txt | ./forparser

Notes and assumptions
- The grammar is a simplified C-like grammar for the purpose of syntax validation only. It accepts assignments, nested for-loops, while and do-while loops, blocks ({}), ++/-- in increment, and simple expressions using + and -.
- The grammar is a simplified C-like grammar for the purpose of syntax validation only. It accepts assignments, declarations (`int`), nested loops (for/while/do-while), blocks ({}), ++/-- in increment, and expressions with +, -, *, / and parentheses. Operator precedence and unary minus are supported.
- This is a syntax checker only — no semantic checks (types, variable declarations, etc.).

Sample inputs are provided in `sample_inputs.txt` to try both valid and invalid examples.

If you'd like, I can try to build and run the parser here (if you want me to invoke a terminal command), or expand the grammar to accept more C constructs, add better expression parsing (precedence), or include tests that run automatically.
