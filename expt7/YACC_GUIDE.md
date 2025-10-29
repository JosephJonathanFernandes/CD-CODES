# YACC/Bison + Flex — Practical Guide and API Cheatsheet

This one-pager explains how YACC/Bison (parser) works with Flex (lexer), the key functions involved, and how to apply them using the examples in this folder.

---

## Overview: Who does what?

- Flex (lexer) reads characters and groups them into tokens. It returns a token code to the parser and can attach a semantic value via `yylval`.
- Bison/YACC (parser) reads the token stream from `yylex()` and matches it against grammar rules; each rule may execute C code (semantic action).
- Your `main()` calls `yyparse()`; the parser calls `yylex()` as needed; on syntax errors it calls `yyerror()`.

Generated files
- `bison -d file.y` → `file.tab.c` (parser) + `file.tab.h` (token declarations)
- `flex file.l` → `lex.yy.c` (lexer)
- Compile/link both (and any support C files) into an executable.

---

## Minimal contracts (must-know)

- `int yylex(void);`
  - Implemented by Flex. Returns token codes. For token with a value (like `NUM`), set `yylval = ...` before returning.
- `int yyparse(void);`
  - Implemented by Bison. Drives the parse; calls `yylex()`; returns 0 on success.
- `void yyerror(const char* s);`
  - Your error reporter for syntax/semantic errors.
- `YYSTYPE`
  - The C type of `yylval` (the semantic value). In your examples it’s `int`; often a `%union` is used for multiple types.

---

## Tokens and grammar in Bison

- Declare token kinds in `.y` with `%token` for named tokens. Character literals like `'+'` can be used directly in grammar rules.
- Typical header of `.y`:
  ```c
  %{
  #include <stdio.h>
  #include <stdlib.h>
  int yylex(void);
  void yyerror(const char *s);
  %}

  %token NUM ID INT COMMA SEMICOLON ASSIGN
  ```
- Grammar rules (with actions) use `$1`, `$2`, ... for child values and `$$` for the rule’s result value.

Example (from `expr.y`):
```bison
expr: expr '+' expr { $$ = $1 + $3; }
    | '(' expr ')'  { $$ = $2; }
    | NUM           { $$ = $1; }
    ;
```

---

## Precedence and associativity

Bison resolves many shift/reduce conflicts via precedence declarations:
- `%left '+' '-'`
- `%left '*' '/'`
- `%right UMINUS`
- `%nonassoc` (neither left nor right)

Use `%prec` to assign a particular precedence to a production, e.g. unary minus:
```bison
expr: '-' expr %prec UMINUS { $$ = -$2; };
```

This is how `expr.y` and `assign.y` get correct arithmetic behavior without extra nonterminals.

---

## Semantic values: `yylval`, `YYSTYPE`, `%union`

- In your examples, `#define YYSTYPE int` (or similar) makes `yylval` an int.
- For richer ASTs, use a union:
  ```bison
  %union {
    int    ival;
    char*  sval;
    /* structs for AST nodes, etc. */
  }
  %token <ival> NUM
  %token <sval> ID
  %type  <ival> expr
  ```
- In the lexer, set the right field of `yylval`:
  ```c
  [0-9]+  { yylval.ival = atoi(yytext); return NUM; }
  [a-zA-Z][a-zA-Z0-9]* { yylval.sval = strdup(yytext); return ID; }
  ```

---

## Error handling

- `yyerror(const char* s)` is called on syntax errors. You decide what to print/log.
- Error recovery: Add the special token `error` to the grammar to skip bad input and continue.
  ```bison
  line: expr '\n'
      | error '\n' { yyerrok; }  /* discard to end-of-line */
      ;
  ```
- `yyerrok` resets the error status; `yyclearin` discards the lookahead token.

`expr.y` and `binexpr.y` mostly fail-fast or print a message. `decl.y` prints “Invalid declaration” via `yyerror`.

---

## Flex essentials (lexer)

- Flex rule skeleton:
  ```flex
  %%
  [0-9]+    { yylval = atoi(yytext); return NUM; }
  [ \t]+    ;                   /* skip whitespace */
  "\n"     { return '\n'; }
  "+"      { return '+'; }
  .        { return yytext[0]; }
  %%
  int yywrap(void) { return 1; } // avoid linking -lfl on Windows
  ```
- `yytext` holds the matched lexeme; `yyleng` its length.
- `yyin`/`yyout` are `FILE*`s for input/output (default: stdin/stdout). You can set `yyin = fopen("file.txt", "r");` before `yyparse()` to read from a file.

Common Flex helper APIs (optional, from Flex runtime):
- `YY_BUFFER_STATE yy_scan_string(const char* s);`
- `YY_BUFFER_STATE yy_create_buffer(FILE* f, int size);`
- `void yy_switch_to_buffer(YY_BUFFER_STATE b);`
- `void yy_delete_buffer(YY_BUFFER_STATE b);`
- `void yyrestart(FILE* f);` (reset scanner to new FILE)

---

## Parser debugging and better errors

- Generate state report: `bison -v file.y` → `file.output` with states and conflicts.
- Enable runtime debug traces:
  ```c
  /* in .y */
  %define parse.trace
  /* in C code */
  extern int yydebug; int yydebug = 1;
  ```
- Nicer messages: `#define YYERROR_VERBOSE` (older) or `
  %define parse.error detailed
  ` (newer Bison) for explanatory errors.

---

## Typical Windows build (PowerShell)

```powershell
bison -d expr.y
flex expr.l
gcc lex.yy.c expr.tab.c -o expr.exe
.\expr.exe
```

Why no `-lfl`? Each lexer here defines:
```c
int yywrap(void) { return 1; }
```
which satisfies the Flex runtime’s end-of-input hook.

---

## Common function/reference list

Parser side (Bison):
- `int yyparse(void);` — start parse
- `void yyerror(const char* s);` — syntax/semantic error callback
- `int yylex(void);` — provided by lexer
- `int yydebug;` — set to 1 to enable debug traces (if compiled with trace)
- `yyerrok; yyclearin;` — error recovery macros used in grammar actions

Lexer side (Flex):
- `int yylex(void);` — main scanner function
- `int yywrap(void);` — return 1 at EOF (can be your stub)
- `FILE* yyin, *yyout;` — input/output streams (set before parsing)
- `char* yytext; int yyleng;` — current lexeme text and length
- Buffer management: `yy_scan_string`, `yy_create_buffer`, `yy_switch_to_buffer`, `yy_delete_buffer`, `yyrestart`

Semantic values:
- `YYSTYPE yylval;` — global semantic value set by `yylex`, read by `yyparse`
- `%union` and typed tokens (`<field>` annotations) for multi-type values

---

## Patterns illustrated by this repo

- Arithmetic with precedence and unary minus (`expr.y`, `assign.y`) using `%left/%right` and `%prec UMINUS`.
- Keyword vs identifier in lexer using string compare (`decl.l`: returns `INT` when `yytext=="int"`, else `ID`).
- Strict line-based patterns (`binexpr.y` requires `NUM op NUM` followed by `\n`).
- Printing semantic results in actions (e.g., `printf("Result = %d\n", $1);`).

---

## Extending these examples (ideas)

- Add variables to `expr.y` using a symbol table: on `ID` lookups, fetch stored value; on assignments, store value.
- Switch to `%union` to support both numbers and identifier strings cleanly.
- Add error recovery with the `error` token to skip bad lines and continue parsing.
- Parse from files: set `yyin = fopen("input.txt", "r");` before `yyparse()` to process a file.

---

## Tiny starter templates

Lexer template (`.l`):
```flex
%{
#include "parser.tab.h"
#include <stdlib.h>
int yywrap(void){ return 1; }
%}
%%
[0-9]+      { yylval = atoi(yytext); return NUM; }
[ \t]+      ;
"\n"        { return '\n'; }
.           { return yytext[0]; }
%%
```

Parser template (`.y`):
```bison
%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char* s) { fprintf(stderr, "Error: %s\n", s); }
%}
%token NUM
%%
input: /* empty */ | input line ;
line: expr '\n' { printf("= %d\n", $1); } ;
expr: expr '+' expr { $$ = $1 + $3; }
    | NUM ;
%%
int main(){ return yyparse(); }
```

Use your existing `.l/.y` as richer references.

---

## See also

- Bison manual (latest): https://www.gnu.org/software/bison/manual/
- Flex manual: https://westes.github.io/flex/manual/

This guide is tailored to your current lab — open `expr.y`, `decl.y`, `binexpr.y`, and `assign.y` side-by-side with this file to connect concepts with working code.
