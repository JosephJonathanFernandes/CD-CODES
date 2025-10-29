# Expression Parser (`expr.y`) and Lexer (`expr.l`) — Explained

This note explains the full expression evaluator, now with floating-point math, variables with assignment, prefix/postfix ++/-- on identifiers, exponentiation (^) and modulo (%), along with error handling that suppresses output on bad lines.

---

## What it does

- Parses and evaluates arithmetic expressions over doubles (floats and ints).
- Supports: `+  -  *  /  %  ^  ( )` and unary minus.
- Variables and simple assignment: `name = expr`.
- Prefix/postfix inc/dec on identifiers: `++x, --x, x++, x--`.
- On division or modulo by zero, prints an error and does not print a result for that line.
- Prints the result when a newline (`\n`) is read (unless an error occurred on that line).

Examples
```text
Input:  3 + 4 * 5\n            → Result = 23
Input:  1/2\n                   → Result = 0.5
Input:  x = 5\n               → x = 5
Input:  --x\n                  → Result = 4
Input:  2 ^ 3 ^ 2\n         → Result = 512   (right-associative)
Input:  5.5 % 2\n            → Result = 1.5
Input:  7 / 0\n               → Error: division by zero  (no result line)
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
void yyerror(const char*); // error reporter (also sets a per-line error flag)
```

Semantic values and tokens
```bison
%union { double d; int sym; }

%token <d> NUM
%token <sym> ID
%token INC DEC
%left '+' '-'
%left '*' '/' '%'
%right UMINUS
%right '^'

%type <d> expr
```
- `%union` carries either a double (`d`) or a symbol index (`sym`).
- `ID` tokens carry a symbol index into a tiny symbol table.
- `INC`/`DEC` are tokens for `++` and `--`.

Grammar and actions (core rules, simplified)
```bison
input: /* empty */ | input line ;

line:  expr '\n'              { if (!had_error_line) printf("Result = %g\n", $1); had_error_line = 0; }
    |  ID '=' expr '\n'       { if (!had_error_line) { syms[$1].val = $3; printf("%s = %g\n", syms[$1].name, syms[$1].val); } had_error_line = 0; }
    |  error '\n'             { had_error_line = 0; yyerrok; }
    ;

expr:  expr '+' expr           { $$ = $1 + $3; }
  |  expr '-' expr           { $$ = $1 - $3; }
  |  expr '*' expr           { $$ = $1 * $3; }
  |  expr '/' expr           { if ($3 == 0.0) { yyerror("division by zero"); $$ = 0.0; } else $$ = $1 / $3; }
  |  expr '%' expr           { if ($3 == 0.0) { yyerror("modulo by zero"); $$ = 0.0; } else $$ = fmod($1, $3); }
  |  expr '^' expr           { $$ = pow($1, $3); }        // right-associative
  |  '-' expr %prec UMINUS   { $$ = -$2; }
  |  '(' expr ')'            { $$ = $2; }
  |  NUM                     { $$ = $1; }
  |  ID                      { $$ = syms[$1].val; }
  |  INC ID                  { syms[$2].val += 1.0; $$ = syms[$2].val; } // ++x
  |  DEC ID                  { syms[$2].val -= 1.0; $$ = syms[$2].val; } // --x
  |  ID INC                  { $$ = syms[$1].val; syms[$1].val += 1.0; } // x++
  |  ID DEC                  { $$ = syms[$1].val; syms[$1].val -= 1.0; } // x--
  ;
```
- `$$` is the value produced by the rule; `$1`, `$2`, `$3` are child values.
- Division/modulo by zero set a line error via `yyerror` and suppress printing.
- `%prec UMINUS` ties unary minus to a high precedence so `-3*2` parses as `(-3) * 2`.
- `^` is right-associative by declaration; `2 ^ 3 ^ 2` parses as `2 ^ (3 ^ 2)`.

Error handling
```c
void yyerror(const char *s) {
  had_error_line = 1;
  fprintf(stderr, "Error: %s\n", s);
}
```
- Called by Bison on syntax errors or manually by actions (e.g., division/modulo by zero).
- `had_error_line` prevents printing a `Result` for the current line; the parser then recovers on newline.

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
- Includes `expr.tab.h` so it knows token codes and `%union` layout.
- Defines `int yywrap(void){ return 1; }` so Windows builds don’t need `-lfl`.

Core rules (conceptual)
```flex
[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?  { yylval.d = strtod(yytext, NULL); return NUM; }
\.[0-9]+([eE][+-]?[0-9]+)?           { yylval.d = strtod(yytext, NULL); return NUM; }
[A-Za-z_][A-Za-z0-9_]*               { yylval.sym = lookup(yytext); return ID; }
"++"    { return INC; }
"--"    { return DEC; }
[ \t]+  ;                 // skip spaces/tabs
"\n"    { return '\n'; }   // end-of-line triggers printing
"+"     { return '+'; }
"-"     { return '-'; }
"*"     { return '*'; }
"/"     { return '/'; }
"%"     { return '%'; }
"^"     { return '^'; }
"("     { return '('; }
")"     { return ')'; }
.       { return yytext[0]; } // any other single char
```
- `yytext` is the matched lexeme; numbers are parsed via `strtod`.
- The lexer doesn’t print anything; it only identifies tokens for the parser.

---

## Step-by-step example

Input: `3 + 4 * 5\n`
1) Lexer returns tokens → `NUM(3)`, `'+'`, `NUM(4)`, `'*'`, `NUM(5)`, `'\n'`.
2) Parser reduces `4 * 5` first because `*` has higher precedence than `+`.
3) Then reduces `3 + 20` to `23`.
4) On `'\n'`, rule `line: expr '\n'` prints `Result = 23`.

Unary minus example: `-3 + 2\n` → `Result = -1`.

Inc/dec examples (stateful per session):
```
x = 5\n   → x = 5
--x\n    → Result = 4
x--\n    → Result = 4   (x becomes 3)
```

Division/modulo-by-zero example: `7 / 0\n`
- Action detects zero, calls `yyerror("division by zero")`; no `Result` line is printed for that input.

---

## Build and run (PowerShell)

```powershell
bison -d expr.y
flex expr.l
gcc lex.yy.c expr.tab.c -o expr.exe
.\expr.exe
# Try a few:
# echo "3 + 4 * 5" | .\expr.exe
# echo "1/2" | .\expr.exe
# echo "x = 5`n--x" | .\expr.exe
# echo "2 ^ 3 ^ 2" | .\expr.exe
# echo "5.5 % 2" | .\expr.exe
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
- Divide/modulo-by-zero suppress `Result` for that line; only an error is printed to stderr.
- `--5` is a syntax error: inc/dec apply to identifiers only.
- Right-associativity of `^`: `2 ^ 3 ^ 2` is `2 ^ (3 ^ 2)`.

---

## Where to go next

- Add functions like `sin`, `cos`, etc.
- Add comparison/logical operators.
- Enable parser tracing (`%define parse.trace`) to see shift/reduce steps during debugging.

For broader YACC/Flex concepts and APIs, see `YACC_GUIDE.md`. For a lab-wide summary and viva prompts, see `PRESENTATION.md`.
