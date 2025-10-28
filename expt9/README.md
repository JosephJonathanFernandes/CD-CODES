# YACC + LEX Three-Address Code (TAC) generator

This small project implements a YACC (Bison) grammar and a Flex lexer to parse arithmetic expressions, assignments and while loops and generate Three-Address Code (TAC).

Files added:
- `grammar.y` - YACC/Bison grammar with semantic actions that emit TAC. Produces `y.tab.c`/`y.tab.h` when run with Bison.
- `lexer.l` - Flex lexical analyzer that tokenizes IDs, NUMs, keywords and operators.
- `Makefile` - Simple build rules (uses `bison` and `flex`).
- `test1.txt` - sample input (see below).

Requirements
- bison (or yacc-compatible)
- flex (or lex-compatible)
- gcc (or a C compiler)

On Windows
- You can use MSYS2, Cygwin, or WSL to get `bison` and `flex`. If you prefer native Windows builds, install tools that provide these utilities.

Build (PowerShell example using MSYS/WSL-like tools available on PATH):

```powershell
bison -d -y grammar.y; flex lexer.l; gcc -o tac y.tab.c lex.yy.c -lfl
```

Or using the Makefile (if `make` is available):

```powershell
make
```

Run

```powershell
./tac < test1.txt
```

Sample `test1.txt` (example program):

```
sum = 0;
i = 1;
while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}

```

Expected TAC (sample):

L1:
t1 = i <= 5
if t1 == 0 goto L2
t2 = sum + i
sum = t2
t3 = i + 1
i = t3
goto L1
L2:

Notes
- The implementation uses simple string temporaries (`t1`, `t2`, ...) and labels (`L1`, `L2`, ...). It's intentionally minimal for educational purposes.
- For larger projects consider storing TAC in a data structure for further optimizations and pretty-printing.
