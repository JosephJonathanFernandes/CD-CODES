# Assignment Parser (`assign.y`) and Lexer (`assign.l`) — Explained

Updated: Supports multi-type assignments (int, float, char, string, boolean) and evaluates numeric expressions. This page explains what it parses, how it’s implemented, and exactly how to build/run it on Windows (PowerShell).

---

## What it does

- Parses `ID = <rhs> ;` where `<rhs>` can be:
     - Numeric expression over ints and floats: `+ - * / ( )` and unary minus
     - Character literal: `'A'` (simple form)
     - String literal: `"hello"` (with common escapes handled)
     - Boolean literal: `true` | `false`
- Prints `name = value`. Numeric values are printed without a trailing `.0` when integral (e.g., `7`).

Example
```text
Input:  x = 3 * (2 + 1);
Output: x = 9
```

---

## How the pieces talk

- `main()` in `assign.y` prints a short help then calls `yyparse()`.
- The parser asks the lexer (`yylex`) for tokens such as `ID`, `NUM`, `FLOAT`, `CHARLIT`, `STRING`, `TRUE`, `FALSE`, `ASSIGN (=)`, `SEMICOLON (;)`, and operators.
- Semantic values are typed via `%union`:
     - `ID`, `STRING` → `char*`
     - `NUM` → `int`
     - `FLOAT` → `double`
     - `CHARLIT` → `char`
     - `TRUE`/`FALSE` → `int` (0/1)

---

## Inside the parser: `assign.y`

Key grammar (accurate to source):

```bison
%union {
     int    ival;     /* for NUM */
     double fval;     /* for FLOAT and expr */
     char   cval;     /* for CHARLIT */
     int    bval;     /* 0/1 for FALSE/TRUE */
     char  *sval;     /* for ID and STRING */
}

%type <fval> expr
%left '+' '-'
%left '*' '/'
%right UMINUS

stmt:
               ID ASSIGN expr     SEMICOLON  { /* prints as int if integral */ }
          | ID ASSIGN CHARLIT  SEMICOLON
          | ID ASSIGN STRING   SEMICOLON
          | ID ASSIGN TRUE     SEMICOLON
          | ID ASSIGN FALSE    SEMICOLON
          ;

expr:
               expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr      /* guarded div-by-zero (prints error, yields 0) */
          | '-' expr %prec UMINUS
          | '(' expr ')'
          | NUM                /* cast to double */
          | FLOAT
          ;

void yyerror(const char *s) { fprintf(stderr, "Error: %s\n", s); }
```

Notes
- Division by zero is detected with a small epsilon check using `fabs`.
- When printing numeric results, the code avoids a trailing `.0` by checking if the double is integral. IDs and strings are freed to avoid leaks.

---

## Inside the lexer: `assign.l`

Highlights
- Returns typed tokens consistent with `%union`:
     - Booleans: `true`/`false` → `TRUE`/`FALSE` with `bval` set
     - Floats (incl. exponent forms) → `FLOAT` using `strtod`
     - Integers (incl. optional exponent) → `NUM` via `strtol`
     - Char literal (simple `'c'` form) → `CHARLIT`
     - String literal with escapes → `STRING` (quotes stripped, escapes unescaped)
     - Identifiers → `ID` (duplicated string)
- Operators and punctuation are returned as literal characters or specific tokens (`ASSIGN`, `SEMICOLON`).
- `yywrap()` returns 1, so no extra link library is needed on Windows.

---

## Step-by-step example

Input: `x = 3 * (2 + 1);`
1) Lexer: `ID("x")`, `ASSIGN('=')`, `NUM(3)`, `'*'`, `'('`, `NUM(2)`, `'+'`, `NUM(1)`, `')'`, `';'`.
2) Parser computes `2 + 1 → 3`, then `3 * 3 → 9`, then matches the assignment rule and prints `x = 9`.

Unary minus example: `y = -4 + 6;` → `y = 2`.

More examples

```text
pi = 3.14159;      → pi = 3.14159
c = 'A';           → c = 'A'
msg = "Hi";        → msg = "Hi"
ok = true;         → ok = true
```

Division-by-zero: `z = 7 / 0;` → prints `Error: division by zero` then `z = 0`.

---

## Build and run (Windows PowerShell)

```powershell
# Generate parser/lexer
bison -d assign.y
flex assign.l

# Compile (link math for fabs)
gcc assign.tab.c lex.yy.c -o assign.exe -lm

# Run interactively
.\assign.exe

# Or pipe a quick test
Write-Output "x = 3 * (2 + 1); y = 3.14;" | .\assign.exe
Write-Output 's = "hi"; c = '\''A'\''; b = false;' | .\assign.exe
```

Notes
- Press Ctrl+Z then Enter to quit interactive mode.
- No `-lfl` is needed on Windows because `yywrap()` is defined in the lexer.

---

## Pitfalls and limitations

- No symbol table: assignments are not stored; you can’t use the variable later on the RHS.
- No symbol table: RHS expressions don’t allow identifiers (no variable references).
- Missing `;` or malformed RHS triggers a syntax error via `yyerror`.

## Extensions

- Add a map (symbol table) to store values by name; allow `expr` to use `ID` values and do type checking.
- Support compound assignments (`+=`, `-=`, etc.).
- Add error recovery (`error` token) to skip to next `;` and continue parsing.
