# Assignment Parser (`assign.y`) and Lexer (`assign.l`) — Explained

This note explains how the assignment example works. It parses statements like `x = 3 * (2 + 1);`, evaluates the right-hand side, and prints `x = 9`.

---

## What it does

- Parses `ID = <expression> ;` statements.
- Evaluates the integer expression on the right-hand side (supports +, -, *, /, parentheses, unary minus).
- Prints the identifier name and computed value.

Example
```text
Input:  x = 3 * (2 + 1);
Output: x = 9
```

---

## How the pieces talk

- `main()` in `assign.y` calls `yyparse()`.
- The parser calls the lexer `yylex()` to obtain tokens like `ID`, `NUM`, `ASSIGN` (`=`), `SEMICOLON`, and operators.
- For each `ID`, the lexer copies the lexeme text into a global `char id_name[64]` so the parser can print it in the assignment action.

---

## Inside the parser: `assign.y`

Header and contracts
```c
#define YYSTYPE int
extern char id_name[];   // set by the lexer when ID is scanned
int yylex(void);
void yyerror(const char *s);
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
- Saves the current identifier text into a global buffer `id_name[64]` whenever an `ID` is matched.
- Sets `yylval` for `NUM` tokens via `atoi(yytext)`.
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
- Only integer arithmetic is supported.
- Missing `;` or malformed RHS triggers a syntax error via `yyerror`.

## Extensions

- Add a map (symbol table) to store values by name; allow `expr` to use `ID` values.
- Switch to `%union` to carry both numbers and identifier strings cleanly.
- Add error recovery (`error` token) to skip to next `;` and continue parsing.
