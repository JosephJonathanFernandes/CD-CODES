YACC/Flex: Validate basic and nested for-loops with assignments

Files provided
- for.y         — Bison/YACC grammar (parser)
- for.l         — Flex/Lex scanner (tokenizer)
- sample_inputs.txt — Example inputs (valid and invalid)

Goal
Validate syntax of a basic for loop as well as nested for loops with assignment statements.
Note: The grammar also supports while and do-while loops, simple `int` declarations, and expressions with operator precedence and unary minus. These extras are harmless and can be ignored if your assignment only asks for `for`.

How it works (contract)
- Input: a C-like snippet containing assignment statements and `for`-loops (nesting allowed). Blocks `{ ... }` are supported.
- Output: For each program snippet (separated by a line with `###`), the parser prints either `Program: syntactically correct.` or `Program: has syntax errors.`; any syntax errors include the line number.
- Error modes: syntax errors are reported via `yyerror` with the current `yylineno`.

Quick try (Windows, using included binary)

```powershell
cd "c:\Users\Joseph\Desktop\compiler design\expt8"
Get-Content .\sample_inputs.txt | .\for.exe | Tee-Object -FilePath .\parser_output.txt
```

This will create `parser_output.txt` with the validation results for each snippet separated by `###`.

Building and running (Windows notes)

Prerequisites (one of the options):
- Install Win flex-bison (https://github.com/westes/flex/tree/master) and a GCC toolchain like MinGW or MSYS2.
- Or use WSL (Windows Subsystem for Linux) with flex and bison installed.

Recommended steps (PowerShell; adapt if using WSL):

1) Using GNU tools (winflexbison / mingw) installed and on PATH
    - cd to the folder:
       ```powershell
       cd "c:\Users\Joseph\Desktop\compiler design\expt8"
       ```
    - Generate parser and scanner:
       ```powershell
       bison -d -v .\for.y      # generates for.tab.c and for.tab.h
       flex .\for.l             # generates lex.yy.c
       ```
    - Compile:
       ```powershell
       gcc -o for.exe .\for.tab.c .\lex.yy.c -lfl
       # If -lfl fails on Windows, try without it or link the flex library that your toolchain provides
       ```

2) Using WSL (Ubuntu) — open WSL shell and run inside project folder
   bison -d for.y
   flex for.l
   gcc -o forparser for.tab.c lex.yy.c -lfl

Run
- Then feed a source:
   ```powershell
   Get-Content .\sample_inputs.txt | .\for.exe
   ```

Notes and assumptions
- The grammar is a simplified C-like grammar for syntax validation only. It accepts assignments, nested `for`-loops, while/do-while (extra), blocks `{}`, `++/--` in the increment part, and expressions with `+ - * /` and parentheses. Operator precedence and unary minus are supported.
- This is a syntax checker only — no semantic checks (types, variable declarations, etc.).

Sample inputs are provided in `sample_inputs.txt` to try both valid and invalid examples.

If you'd like, I can try to build and run the parser here (if you want me to invoke a terminal command), or expand the grammar to accept more C constructs, add better expression parsing (precedence), or include tests that run automatically.
