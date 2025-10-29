# Strict Binary Expression (`binexpr.y`) and Lexer (`binexpr.l`) — Explained

This example enforces exactly two operands with one operator per input line, now supporting both integers and floating-point numbers (including signs and scientific notation). Operators supported: +, -, *, /, %, ^.

---

## What it does

- Accepts only lines of the form: `NUM op NUM` followed by a newline (`\n`).
- Supported ops: `+  -  *  /  %  ^`.
- Numbers can be:
     - Integers (e.g., `12`, `-3`)
     - Floats (e.g., `12.5`, `.75`, `-0.5`)
     - Scientific notation (e.g., `1e2`, `-3.5E-1`, `+2.0e+3`)
- Spaces around operands/operator are optional.
- Windows newlines (`\r\n`) are handled transparently.
- Prints parsed form and result; division by zero and modulo by zero print clear errors.

Example
```text
Input:  12.5 * 2\n
Output: Parsed: 12.5 * 2 => Result = 25
```

---

## How the pieces talk

- `main()` in `binexpr.y` calls `yyparse()`.
- The parser repeatedly calls the lexer `yylex()` for tokens: `NUM`, operators, and newline `\n`.
- Each valid line must end with a newline to match a grammar rule and trigger output.

---

## Inside the parser: `binexpr.y`

Header and value type
```c
%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int yylex(void);
void yyerror(const char *s);
/* print helper that prints integers without trailing .0 */
static void print_num(double v) {
     long long iv = (long long)v;
     if (v == (double)iv) printf("%lld", iv); else printf("%g", v);
}
%}
%define api.value.type {double}
```

Tokens
```bison
%token NUM
```

Grammar and actions (strict patterns only)
```bison
input: /* empty */ | input line ;

line:  NUM '+' NUM '\n'  { ... print + ... }
     |  NUM '-' NUM '\n'  { ... print - ... }
     |  NUM '*' NUM '\n'  { ... print * ... }
     |  NUM '/' NUM '\n'  { if ($3==0.0) { printf("Error: division by zero\n"); } else { ... print / ... } }
     |  NUM '%' NUM '\n'  { if ($3==0.0) { printf("Error: modulo by zero\n"); } else { ... print % ... } }
     |  NUM '^' NUM '\n'  { ... print ^ ... }
     ;
```
- Only the four exact patterns are allowed; not a general expression grammar.
- Newline (`'\n'`) is part of each rule; without it the line doesn’t match.

Error handling
```c
void yyerror(const char *s) { fprintf(stderr, "Invalid input\n"); }
```

---

## Inside the lexer: `binexpr.l`

Highlights
```flex
%{
#include "binexpr.tab.h"
#include <stdlib.h>
int yywrap(void){ return 1; }
%}

[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?  { yylval = strtod(yytext, NULL); return NUM; }
[ \t]+     ;                    /* skip spaces/tabs */
"\r\n"     { return '\n'; }       /* Windows CRLF */
"\n"       { return '\n'; }
"\r"       ;                    /* stray CR -> skip */
"+"         { return '+'; }
"-"         { return '-'; }
"*"         { return '*'; }
"/"         { return '/'; }
.            { return yytext[0]; }
```
- Supplies signed integers/floats (with exponent), operators, and newline token.
- CRLF is normalized to a single `'\n'` for the grammar.

---

## Examples

- `12 + 5\n` → `Parsed: 12 + 5 => Result = 17`
- `12.5 * 2\n` → `Parsed: 12.5 * 2 => Result = 25`
- `-3 - -4.5\n` → `Parsed: -3 - -4.5 => Result = 1.5`
- `+1.0e2 / 4e1\n` → `Parsed: 100 / 40 => Result = 2.5`
- `5 % 2\n` → `Parsed: 5 % 2 => Result = 1`
- `2 ^ 3\n` → `Parsed: 2 ^ 3 => Result = 8`
- `7 / 0\n` → `Error: division by zero`
- `5 % 0\n` → `Error: modulo by zero`
- `3 + 4 + 5\n` → Invalid (doesn’t match any strict rule)

---

## Build and run (PowerShell)

```powershell
bison -d binexpr.y
flex binexpr.l
gcc lex.yy.c binexpr.tab.c -o binexpr.exe
\.\binexpr.exe
# Example
# echo "12 + 5" | .\binexpr.exe
```

Notes
- Each input must end in a newline to trigger a `line` rule.
- No `-lfl` needed because `yywrap()` is defined in the lexer.
- On PowerShell, quote the input so `+` is not interpreted by the shell: `echo "12 + 5" | .\binexpr.exe`

---

## Pitfalls and extensions

Pitfalls
- Inputs like `3 + 4 * 5` or `(3 + 4)` are invalid here by design.
- Missing newline won’t trigger evaluation.

Extensions
- Generalize to a full expression grammar with precedence (see `expr.y`).
- Add modulo (`%`) with well-defined semantics for doubles (e.g., using `fmod`).
- Add error recovery to skip to next newline on invalid input.
