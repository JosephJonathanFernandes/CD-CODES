# Expression Parser (`expr.y`) and Lexer (`expr.l`) — Explained

This note explains how the expression evaluator in this folder works, tying together the Bison/YACC parser (`expr.y`) and the Flex lexer (`expr.l`). Use it for viva or as a quick refresher.

---

## What it does

- Parses and evaluates integer arithmetic expressions.
- Supports: `+  -  *  /  ( )` and unary minus.
- Prints the result when a newline (`\n`) is read.

Example
```text
Input:  3 + 4 * 5\n
Output: Result = 23
```

---

## How the pieces talk

- `main()` in `expr.y` calls `yyparse()`.
- `yyparse()` (parser) repeatedly calls `yylex()` (lexer) to get tokens.
- The lexer returns token kinds like `NUM`, `+`, `-`, `*`, `/`, `(`, `)`, and `\n`.
- For `NUM`, the lexer sets `yylval` (an `int`) to the integer value.
- When the parser reduces a grammar rule, it runs C code to compute the value using `$$`, `$1`, `$2`, `$3`, etc.

---

## Inside the parser: `expr.y`

Header contracts
```c
int yylex(void);           // provided by the lexer
void yyerror(const char*); // your error reporter
#define YYSTYPE int        // semantic value type is int
```

Token and precedence declarations
```bison
%token NUM
%left '+' '-'
%left '*' '/'
%right UMINUS
```
- `%left` / `%right` assign precedence and associativity to operators.
- `UMINUS` is a fake token name used to give unary minus a higher precedence via `%prec`.

Grammar and actions (core rules, simplified)
```bison
input: /* empty */ | input line ;

line:  expr '\n'        { printf("Result = %d\n", $1); } ;

expr:  expr '+' expr     { $$ = $1 + $3; }
     | expr '-' expr     { $$ = $1 - $3; }
     | expr '*' expr     { $$ = $1 * $3; }
     | expr '/' expr     { if ($3 == 0) { yyerror("division by zero"); $$ = 0; } else $$ = $1 / $3; }
     | '-' expr %prec UMINUS { $$ = -$2; }
     | '(' expr ')'      { $$ = $2; }
     | NUM               { $$ = $1; }
     ;
```
- `$$` is the value produced by the rule; `$1`, `$2`, `$3` are child values.
- Division-by-zero is handled in the action and reported through `yyerror`.
- `%prec UMINUS` ties the unary-minus rule to the high precedence of `UMINUS` so `-3*2` parses as `(-3) * 2`.

Error handling
```c
void yyerror(const char *s) { fprintf(stderr, "Error: %s\n", s); }
```
- Called automatically by Bison on syntax errors or manually by your actions (e.g., division by zero).

Main
```c
int main(void) {
  printf("Enter expression (press Ctrl+Z then Enter to quit on Windows)\n");
  yyparse();
  return 0;
}
```

---

## Inside the lexer: `expr.l`

Header notes
- Includes `expr.tab.h` so it knows token codes like `NUM`.
- Defines `int yywrap(void){ return 1; }` so Windows builds don’t need `-lfl`.

Core rules (conceptual)
```flex
[0-9]+   { yylval = atoi(yytext); return NUM; }
[ \t]+  ;                 // skip spaces/tabs
"\n"    { return '\n'; }   // end-of-line triggers printing
"+"     { return '+'; }
"-"     { return '-'; }
"*"     { return '*'; }
"/"     { return '/'; }
"("     { return '('; }
")"     { return ')'; }
.       { return yytext[0]; } // any other single char
```
- `yytext` is the matched lexeme; `atoi(yytext)` converts digits to an int.
- The lexer doesn’t print anything; it only identifies tokens for the parser.

---

## Step-by-step example

Input: `3 + 4 * 5\n`
1) Lexer returns tokens → `NUM(3)`, `'+'`, `NUM(4)`, `'*'`, `NUM(5)`, `'\n'`.
2) Parser reduces `4 * 5` first because `*` has higher precedence than `+`.
3) Then reduces `3 + 20` to `23`.
4) On `'\n'`, rule `line: expr '\n'` prints `Result = 23`.

Unary minus example: `-3 + 2\n`
- `- 3` reduces via the `%prec UMINUS` rule to `(-3)`, then `(-3) + 2` → `-1`.

Division-by-zero example: `7 / 0\n`
- Action detects `$3 == 0`, calls `yyerror("division by zero")`, sets `$$ = 0`, and prints `Result = 0`.

---

## Build and run (PowerShell)

```powershell
bison -d expr.y
flex expr.l
gcc lex.yy.c expr.tab.c -o expr.exe
.\expr.exe
# Try a few:
# echo "3 + 4 * 5" | .\expr.exe
# echo "-3 + 2" | .\expr.exe
# echo "(3 + 4) * 5" | .\expr.exe
# echo "7 / 0" | .\expr.exe
```

Notes
- Press Ctrl+Z then Enter to end interactive mode.
- No `-lfl` needed because `yywrap()` is defined in the lexer.

---

## Common pitfalls to remember

- Forgetting the newline: the `line` rule prints only when it sees `'\n'`.
- Precedence without declarations: removing `%left/%right/%prec` will cause conflicts or wrong math.
- Missing `#define YYSTYPE int` (or equivalent) causes type mismatches for `yylval`.
- Not handling divide-by-zero: your code already does, but it’s a common gotcha.

---

## Where to go next

- Add variables: introduce `ID` tokens and a symbol table to support names inside expressions.
- Use `%union` to carry both numbers and strings cleanly.
- Enable parser tracing (`%define parse.trace`) to see shift/reduce steps during debugging.

For broader YACC/Flex concepts and APIs, see `YACC_GUIDE.md`. For a lab-wide summary and viva prompts, see `PRESENTATION.md`.
