# Declaration Validator (`decl.y`) and Lexer (`decl.l`) — Explained

This example validates very simple C-like declarations of the form `int a, b, c;`. It prints `Valid declaration` on success; otherwise `Invalid declaration`.

---

## What it does

- Accepts exactly: the keyword `int`, followed by one or more identifiers separated by commas, and a terminating semicolon.
- Any deviation (missing comma, missing semicolon, unknown keyword, stray character) is considered invalid.

Example
```text
Input:  int a, b, c;
Output: Valid declaration
```

---

## How the pieces talk

- `main()` in `decl.y` calls `yyparse()`.
- The lexer returns tokens `INT`, `ID`, `COMMA`, `SEMICOLON`, and `INVALID` for any other single character.
- On a successful parse, the action prints `Valid declaration`. On failure, `yyerror` prints `Invalid declaration`.

---

## Inside the lexer: `decl.l`

Keyword vs identifier
```flex
[a-zA-Z][a-zA-Z0-9]* { if (strcmp(yytext, "int") == 0) return INT; else return ID; }
","                  { return COMMA; }
";"                  { return SEMICOLON; }
[ \t\n]+              ;       // skip whitespace
.                    { return INVALID; }
int yywrap(void){ return 1; }
```
- The rule for identifiers checks if the lexeme equals `"int"`; if so, returns `INT`, otherwise `ID`.
- Any other single character is marked `INVALID`, which will not fit the grammar and thus cause an error.

---

## Inside the parser: `decl.y`

Header contracts
```c
int yylex(void);
void yyerror(const char *s);
```

Tokens
```bison
%token INT ID COMMA SEMICOLON INVALID
```

Grammar and actions
```bison
decl    : INT varlist SEMICOLON   { printf("Valid declaration\n"); } ;

varlist : ID
        | varlist COMMA ID
        ;
```
- Accepts one or more identifiers separated by commas, after the `INT` keyword, then a `SEMICOLON`.
- Any `INVALID` token or wrong sequence triggers a parse error → `yyerror("...")`.

Error handling
```c
void yyerror(const char *s) { printf("Invalid declaration\n"); }
```

---

## Examples

- Valid
  - `int a;`
  - `int a, b, c;`
- Invalid
  - `int , a;`      (comma without preceding ID)
  - `int a b;`      (missing comma)
  - `float a;`      (only `int` is recognized as a keyword)
  - `int a, ;`      (trailing comma)

---

## Build and run (PowerShell)

```powershell
bison -d decl.y
flex decl.l
gcc lex.yy.c decl.tab.c -o decl.exe
.\decl.exe
# Example
# echo "int a, b, c;" | .\decl.exe
```

Notes
- Whitespace is ignored by the lexer.
- No `-lfl` link is needed because `yywrap()` is defined.

---

## Pitfalls and extensions

Pitfalls (by design of the exercise)
- Only the `int` keyword is supported.
- No initialization is allowed (e.g., `int a = 3;` is invalid here).
- No types like `long`, pointers, arrays, or qualifiers.

Extensions
- Recognize multiple keywords (`int`, `float`, `char`, ...).
- Allow initialization with an expression grammar.
- Add semantic checks (e.g., duplicate names) via a symbol table.
