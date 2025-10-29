# Assignment Parser (`assign.y`) and Lexer (`assign.l`) — Explained

Update (multi-type support): The assignment parser now accepts and prints assignments for ints, floats, chars, strings, and booleans. Numeric RHS expressions are evaluated as doubles; other literal RHS types are accepted and echoed. See examples below.

This note explains how the assignment example works. It parses statements like `x = 3 * (2 + 1);`, evaluates the right-hand side, and prints `x = 9`.

---

## What it does

- Parses `ID = <rhs> ;` statements where `<rhs>` can be:
     - Numeric expression with integers and floats: `+, -, *, /, (), unary -` (evaluated to a number)
     - A single character literal: `'a'`, `'\n'`
     - A string literal: `"hello"` (common escapes handled)
     - A boolean literal: `true` or `false`
- Prints the identifier name and RHS value. Numeric values are printed as integers when exact (e.g., `7` instead of `7.0`).

Example
```text
Input:  x = 3 * (2 + 1);
Output: x = 9
```

---

## How the pieces talk

- `main()` in `assign.y` calls `yyparse()`.
- The parser calls the lexer `yylex()` to obtain tokens like `ID`, `NUM`, `ASSIGN` (`=`), `SEMICOLON`, and operators.
- Tokens now carry typed semantic values via `%union` (e.g., `ID` and `STRING` carry `char*`, `NUM` carries `int`, `FLOAT` carries `double`, `CHARLIT` carries `char`, `TRUE/FALSE` carry `int`). The parser prints using these values; there’s no longer a global `id_name`.

---

## Inside the parser: `assign.y`

Header and contracts
```c
Uses `%union` to type semantic values and adds tokens for `FLOAT`, `CHARLIT`, `STRING`, `TRUE`, and `FALSE`. The assignment rule now has multiple alternatives:

```bison
stmt:
          ID ASSIGN expr     SEMICOLON
     | ID ASSIGN CHARLIT  SEMICOLON
     | ID ASSIGN STRING   SEMICOLON
     | ID ASSIGN TRUE     SEMICOLON
     | ID ASSIGN FALSE    SEMICOLON
     ;
```

`expr` evaluates numeric expressions as `double` and accepts both `NUM` and `FLOAT`.
```

Tokens and precedence
```bison
%token ID NUM ASSIGN SEMICOLON
%left '+' '-'
%left '*' '/'
%right UMINUS
```

Grammar and actions
```bison
input: /* empty */ | input stmt ;

stmt:  ID ASSIGN expr SEMICOLON { printf("%s = %d\n", id_name, $3); } ;

expr:  expr '+' expr     { $$ = $1 + $3; }
     | expr '-' expr     { $$ = $1 - $3; }
     | expr '*' expr     { $$ = $1 * $3; }
     | expr '/' expr     { if ($3 == 0) { yyerror("division by zero"); $$ = 0; } else $$ = $1 / $3; }
     | '-' expr %prec UMINUS { $$ = -$2; }
     | '(' expr ')'      { $$ = $2; }
     | NUM               { $$ = $1; }
     ;
```
- The assignment rule prints the left-hand identifier (`id_name`) and the computed RHS value (`$3`).
- Expressions reuse the same precedence scheme as the full evaluator.

Error handling
```c
void yyerror(const char *s) { fprintf(stderr, "Error: %s\n", s); }
```

---

## Inside the lexer: `assign.l`

Key points
- Returns typed tokens using `%union` fields: `NUM` (int), `FLOAT` (double), `CHARLIT` (char), `STRING` (char*), `TRUE/FALSE` (int), and `ID` (char*).
- Converts string/char escapes (e.g., `\n`, `\t`) and strips quotes for `STRING` and `CHARLIT`.
- Returns tokens for `=`, `;`, operators, and parentheses; skips whitespace.

Core rules (conceptual)
```flex
[a-zA-Z][a-zA-Z0-9]* { strncpy(id_name, yytext, sizeof(id_name)-1); id_name[sizeof(id_name)-1] = '\0'; return ID; }
[0-9]+               { yylval = atoi(yytext); return NUM; }
"="                 { return ASSIGN; }
";"                 { return SEMICOLON; }
"+"|"-"|"*"|"/"     { return yytext[0]; }
"("|")"            { return yytext[0]; }
[ \t\n]+            ;  // skip spaces/tabs/newlines
.                    { return yytext[0]; }
int yywrap(void){ return 1; }
```

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

## Build and run (PowerShell)

```powershell
bison -d assign.y
flex assign.l
gcc lex.yy.c assign.tab.c -o assign.exe
.\assign.exe
# Example
# echo "x = 3 * (2 + 1);" | .\assign.exe
```

Notes
- Press Ctrl+Z then Enter to quit interactive mode.
- No `-lfl` needed due to `yywrap()` stub.

---

## Pitfalls and limitations

- No symbol table: assignments are not stored; you can’t use the variable later on the RHS.
- Numeric expressions don’t allow identifiers yet (no variable references on RHS).
- Missing `;` or malformed RHS triggers a syntax error via `yyerror`.

## Extensions

- Add a map (symbol table) to store values by name; allow `expr` to use `ID` values and do type checking.
- Support compound assignments (`+=`, `-=`, etc.).
- Add error recovery (`error` token) to skip to next `;` and continue parsing.
