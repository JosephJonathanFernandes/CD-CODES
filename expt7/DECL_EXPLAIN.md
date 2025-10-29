# Declaration Validator (`decl.y`) and Lexer (`decl.l`)

This project validates single C-like declaration statements. It supports primitive types, qualifiers, storage classes, struct/union/enum tags, typedef-names, pointers (with qualifiers), arrays, function declarators, and simple initializers.

---

## What it does

- Accepts one or more declaration specifiers (any order):
  - Type specifiers: `void`, `char`, `short`, `int`, `long`, `float`, `double`, `signed`, `unsigned`
  - Type tags and typedef-names: `struct S`, `union U`, `enum E`, and typedef names learned during the same run
  - Type qualifiers and storage classes: `const`, `volatile`, `typedef`, `static`, `extern`, `register`
- Accepts one or more declarators separated by commas, terminated by `;` (e.g., `int a, *p;`).
- Declarators supported:
  - Plain: `x`
  - Pointers (with optional qualifiers after each `*`): `*p`, `* const p`, `* volatile * q`
  - Arrays: `a[10]`, `m[3][4]` (size can be empty or an integer/identifier)
  - Functions and function pointers: `int f()`, `int (*fp)(int, char)`
  - Initializers for non-function declarators: `= <integer|float|char|string|identifier>`
  - Forward declarations: `struct S;`

Examples
```text
int a, b, c;                 -> Valid declaration
float x = 3.14, y;           -> Valid declaration
unsigned long long **pp;     -> Valid declaration
char buf[256];               -> Valid declaration
double m[3][4], *p = 0;      -> Valid declaration
void *ptr;                   -> Valid declaration
char c = 'a';                -> Valid declaration
char c2 = '\n';             -> Valid declaration
int * const p;               -> Valid declaration
struct S;                    -> Valid declaration (forward declaration)
struct S a;                  -> Valid declaration
int a, ;                     -> Invalid declaration (trailing comma)
short [10] a;                -> Invalid declaration (missing identifier before [)
int f() = 3;                 -> Invalid declaration (initializer not allowed for function declarator)
```

---

## How the pieces talk

- `main()` in `decl.y` prompts once and calls `yyparse()` to parse exactly one declaration.
- Lexer tokens:
  - Types: `VOID`, `CHAR`, `SHORT`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `SIGNED`, `UNSIGNED`
  - Qualifiers/storage: `CONST`, `VOLATILE`, `TYPEDEF`, `STATIC`, `EXTERN`, `REGISTER`
  - Tags and typedef-names: `STRUCT`, `UNION`, `ENUM`, `TYPE_NAME`
  - Literals: `NUMBER`, `FLOATCONST` (supports 1e-3, .5, 3., 3.14), `CHARCONST` (supports escapes), `STRINGLIT`
  - Punctuation: `COMMA`, `SEMICOLON`, `ASSIGN`, `ASTERISK`, `LBRACKET`, `RBRACKET`, `LPAREN`, `RPAREN`
  - Identifiers: `ID`; others: `INVALID`
- Parser prints `Valid declaration` only if no errors were reported; on any syntax/semantic error `yyerror` prints `Invalid declaration`.

---

## Inside the lexer: `decl.l`

Highlights
- Recognizes keywords for types/qualifiers/storage and tags.
- Typedef-name tracking: after seeing `typedef`, all following identifiers up to the next `;` are recorded as typedef names and returned as `TYPE_NAME`. Because the program parses only a single declaration per run, typedef-names are practically scoped to that one declaration.
- Literals:
  - Integers (`NUMBER`)
  - Floats: `digits.digits`, `.digits`, `digits.` with optional exponent (`FLOATCONST`)
  - Chars with escapes (`CHARCONST`), and strings (`STRINGLIT`)
- Punctuation and identifiers as expected; whitespace is skipped.

---

## Inside the parser: `decl.y`

Key nonterminals
- `decl_specifiers`: storage classes, qualifiers, and type specifiers (including tags and typedef-names)
- `declarator`: pointer(s) + direct declarator (ID, arrays `[]`, functions `()`); function-ness tracked via a semantic attribute
- `init_declarator`: allows `declarator = initializer` only when declarator is not a function (checked semantically)
- `initializer`: `NUMBER` | `FLOATCONST` | `CHARCONST` | `STRINGLIT` | `ID`
- `pointer`: allows `const`/`volatile` immediately after each `*`

Error handling
```c
static int g_error = 0;              // set on any error
void yyerror(const char *s) {
  g_error = 1;
  printf("Invalid declaration\n");
}
// In the decl production we print Valid only if g_error==0
```

---

## Examples

- Valid
  - `int a;`
  - `float x = 1e-3;`
  - `unsigned long long **pp;`
  - `char s[100] = "hi";`
- Invalid
  - `int , a;`      (comma without preceding ID)
  - `int a b;`      (missing comma)
  - `short [10] a;` (missing identifier before bracket)
  - `int a, ;`      (trailing comma)
  - `int f() = 3;`  (initializer not allowed for function declarator)

---

## Build and run (Windows PowerShell)

```powershell
# Generate parser and lexer
bison -d decl.y
flex decl.l

# Compile (requires MinGW-w64 gcc or similar on PATH)
gcc decl.tab.c lex.yy.c -o decl.exe

# Run once interactively (expects exactly one declaration)
.\decl.exe

# Or pipe a single declaration line
Write-Output "unsigned long long **pp;" | .\decl.exe
```

Notes
- Whitespace is ignored by the lexer.
- No `-lfl` link is needed because `yywrap()` is defined.
- If you don't have gcc on Windows, install MSYS2/MinGW or use another C compiler.
- Typedef names are recognized only within the same declaration (up to the `;`) in this program. The parser accepts exactly one declaration per run, so you cannot declare a typedef and then use it in a second declaration within the same execution.

Known limitations (kept intentionally small)
- No struct/union/enum definitions (only tags like `struct S`)
- Parameter lists are syntactically accepted but not semantically validated
- Typedef names are remembered only for the current program run
- No type compatibility checks in initializers; array sizes aren’t validated

---

## Tips
- To inspect parser conflicts:
  - `bison -Wconflicts-sr -Wconflicts-rr -Wcounterexamples -d decl.y`
