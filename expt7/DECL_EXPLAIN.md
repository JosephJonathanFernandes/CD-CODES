# Declaration Validator (`decl.y`) and Lexer (`decl.l`)

This validates C-like declaration statements and now supports many types and forms, not just `int`.

---

## What it does

- Accepts one or more type specifiers: `void`, `char`, `short`, `int`, `long`, `float`, `double`, `signed`, `unsigned` in any reasonable combination (e.g., `unsigned long long int`).
- Accepts one or more declarators separated by commas, terminated by a semicolon `;`.
- Declarators can be:
  - Plain identifiers: `x`
  - Pointers: `*p`, `**q`
  - Arrays: `a[10]`, `m[3][4]` (size is an integer constant or can be left empty)
  - With simple initializer: `= <integer|float|char|identifier>` (semantic type checking is not enforced)
  - Combinations: `int *p, a[10], **q = 0;`

Examples
```text
int a, b, c;                 -> Valid declaration
float x = 3.14, y;           -> Valid declaration
unsigned long long **pp;     -> Valid declaration
char buf[256];               -> Valid declaration
double m[3][4], *p = 0;      -> Valid declaration
void *ptr;                   -> Valid declaration
char c = 'a';                -> Valid declaration
int a, ;                     -> Invalid declaration (trailing comma)
short [10] a;                -> Invalid declaration (missing identifier before [)
char c = '\n';              -> Invalid declaration (escape sequences not enabled)
```

---

## How the pieces talk

- `main()` in `decl.y` calls `yyparse()`.
- The lexer returns tokens for type keywords (`VOID`, `CHAR`, `SHORT`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `SIGNED`, `UNSIGNED`), identifiers (`ID`), numbers (`NUMBER`, `FLOATCONST`, `CHARCONST`), punctuation (`COMMA`, `SEMICOLON`, `ASSIGN`, `ASTERISK`, `LBRACKET`, `RBRACKET`), and `INVALID` for anything unmatched.
- On a successful parse, the action prints `Valid declaration`. On failure, `yyerror` prints `Invalid declaration`.

---

## Inside the lexer: `decl.l`

Highlights
- Recognizes keywords: `void`, `char`, `short`, `int`, `long`, `float`, `double`, `signed`, `unsigned`.
- Tokens for punctuation: `, ; = * [ ]`.
- Literals:
  - Integer constants (`NUMBER`)
  - Float constants in `digits.digits` form (`FLOATCONST`, e.g., `3.14`)
  - Char constants with a single non-escaped character (`CHARCONST`, e.g., `'a'`)
- Identifiers: `ID`.
- Whitespace is skipped.

---

## Inside the parser: `decl.y`

Key nonterminals
- `type_specifier`: sequence of type tokens.
- `declarator`: optional `*` chain + identifier + optional array dimensions.
- `init_declarator`: `declarator` with optional `= initializer`.
- `initializer`: simplified to `NUMBER` | `FLOATCONST` | `CHARCONST` | `ID`.

Error handling
```c
void yyerror(const char *s) { printf("Invalid declaration\n"); }
```

---

## Examples

- Valid
  - `int a;`
  - `float x = 1;`
  - `unsigned long long **pp;`
  - `char s[100];`
- Invalid
  - `int , a;`      (comma without preceding ID)
  - `int a b;`      (missing comma)
  - `short [10] a;` (missing identifier before bracket)
  - `int a, ;`      (trailing comma)

---

## Build and run (PowerShell on Windows)

```powershell
# Generate parser and lexer
bison -d decl.y
flex decl.l

# Compile (requires MinGW-w64 gcc or similar on PATH)
gcc lex.yy.c decl.tab.c -o decl.exe

# Run
./decl.exe
# Or pipe input
"unsigned long long **pp;" | ./decl.exe
```

Notes
- Whitespace is ignored by the lexer.
- No `-lfl` link is needed because `yywrap()` is defined.
- If you don't have gcc on Windows, install MSYS2/MinGW or compile with another C compiler.

Current limitations (by design to keep grammar small)
- Float literals support only `digits.digits` (e.g., `3.14`). No exponent form (`1e-3`) and no `.5`/`3.` forms yet.
- Char literals support a single non-escaped character (e.g., `'a'`). Escape sequences like `'\n'` are not recognized.
- Array sizes can be left empty (e.g., `int a[];`) and are not semantically validated.

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
