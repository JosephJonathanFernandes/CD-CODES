# Lab Session 7 — YACC/Flex Mini-Experiments

Date: October 30, 2025

This folder contains four small, focused examples using Flex (lexer) and Bison/Yacc (parser). They demonstrate tokenization, grammar/precedence, and simple semantic actions.

- `expr.l` / `expr.y` — Expression evaluator with precedence, unary minus, floating-point, variables + assignment, ++/-- on identifiers, %, ^
- `decl.l` / `decl.y` — C-like declaration validator: `int a, b, c;`
- `binexpr.l` / `binexpr.y` — Strict two-operand expressions per line: `num op num` (supports + - * / % ^)
- `assign.l` / `assign.y` — Assignment with expression on RHS (supports + - * / % ^ and unary minus): `x = 3 * (2 + 1);`

---

## How to build and run on Windows (PowerShell)

Tools (verified in `output.txt`): Bison 3.8.2, Flex 2.6.4, GCC 6.3.0.

Notes
- Press Ctrl+Z then Enter to end interactive sessions.
- Each lexer defines `yywrap()` so you don’t need to link `-lfl`.

### Expression evaluator (`expr.*`)

```powershell
bison -d expr.y
flex expr.l
gcc lex.yy.c expr.tab.c -o expr.exe
.\expr.exe
# Example
# echo "3 + 4 * 5" | .\expr.exe
# echo "1/2" | .\expr.exe
# echo "x = 5`n--x" | .\expr.exe
# echo "2 ^ 3 ^ 2" | .\expr.exe
# echo "5.5 % 2" | .\expr.exe
```

### Declaration validator (`decl.*`)

```powershell
bison -d decl.y
flex decl.l
gcc lex.yy.c decl.tab.c -o decl.exe
.\decl.exe
# Example
# echo "int a, b, c;" | .\decl.exe
```

### Strict binary expression (`binexpr.*`)

```powershell
bison -d binexpr.y
flex binexpr.l
gcc lex.yy.c binexpr.tab.c -o binexpr.exe
.\binexpr.exe
# Example
# echo "12 + 5" | .\binexpr.exe
# echo "5 % 2" | .\binexpr.exe
# echo "2 ^ 3" | .\binexpr.exe
```

### Assignment parser (`assign.*`)

```powershell
bison -d assign.y
flex assign.l
gcc lex.yy.c assign.tab.c -o assign.exe
.\assign.exe
# Example
# echo "x = 3 * (2 + 1);" | .\assign.exe
# echo "y = 2 ^ 3;" | .\assign.exe
# echo "z = 5 % 2;" | .\assign.exe
```

---

## 1) `expr.l` / `expr.y` — Full expression evaluator

Purpose
- Parse and evaluate arithmetic expressions with correct precedence and unary minus, printing a result per line. Supports floats, variables/assignment, ++/-- on identifiers, %, ^.

Lexer highlights (`expr.l`)
- Tokens: `NUM` (floats/ints), `ID`, `INC`/`DEC` for ++/--, operators `+ - * / % ^`, parentheses, newline.
- Whitespace `[ \t]+` is ignored.

Grammar and precedence (`expr.y`)
- Precedence and associativity:
  - `%left '+' '-'`
  - `%left '*' '/' '%'`
  - `%right UMINUS`
  - `%right '^'` (right-associative power)
- Core rules:
```
input → input line | ε
line  → expr '\n'           { print Result = $$ }
expr  → expr '+' expr        { $$ = $1 + $3; }
      | expr '-' expr        { $$ = $1 - $3; }
      | expr '*' expr        { $$ = $1 * $3; }
      | expr '/' expr        { if ($3==0) yyerror("division by zero"); else $$=$1/$3; }
      | '-' expr %prec UMINUS { $$ = -$2; }
      | '(' expr ')'         { $$ = $2; }
      | NUM                  { $$ = $1; }
```

Behavior and examples
- `3 + 4 * 5` → `Result = 23` (multiplication before addition)
- `-3 + 2` → `Result = -1`
- `(3 + 4) * 5` → `Result = 35`
- `7 / 0` → `Error: division by zero` (no Result line printed)

Key point to mention
- `%prec UMINUS` disambiguates unary minus vs binary minus and gives it the correct precedence.

---

## 2) `decl.l` / `decl.y` — C-like declaration validator

Purpose
- Accept a simple declaration like `int a, b, c;` and print `Valid declaration`; otherwise `Invalid declaration`.

Lexer highlights (`decl.l`)
- Pattern `[a-zA-Z][a-zA-Z0-9]*` is checked with `strcmp(yytext, "int")` to return `INT` or `ID`.
- Returns `COMMA`, `SEMICOLON`, and for any stray char returns `INVALID`.

Grammar (`decl.y`)
```
decl    → INT varlist SEMICOLON   { printf("Valid declaration\n"); }
varlist → ID | varlist COMMA ID
```

Behavior and examples
- `int a, b, c;` → `Valid declaration`
- `int x;` → `Valid declaration`
- `int , a;` → `Invalid declaration` (comma without ID)
- `int a b;` → `Invalid declaration` (missing comma)
- `float a;` → `Invalid declaration` (lexer only recognizes `int` as keyword)

Key point to mention
- Classic pattern to distinguish keywords from identifiers at the lexer level.

---

## 3) `binexpr.l` / `binexpr.y` — Strict two-operand expressions

Purpose
- Enforce exactly `NUM op NUM` per input line; print the parsed form and result.

Lexer highlights (`binexpr.l`)
- Tokens: `NUM`, literal `+ - * / % ^`, newline. Whitespace is ignored.

Grammar (`binexpr.y`)
```
input → input line | ε
line  → NUM '+' NUM '\n' { print }
  | NUM '-' NUM '\n' { print }
  | NUM '*' NUM '\n' { print }
  | NUM '/' NUM '\n' { check div-by-zero }
  | NUM '%' NUM '\n' { check mod-by-zero }
  | NUM '^' NUM '\n' { print pow }
```

Behavior and examples
- `12 + 5` → `Parsed: 12 + 5 => Result = 17`
- `7 / 0` → `Error: division by zero`

Key point to mention
- Contrasts with `expr.y`: this grammar is intentionally strict and requires a newline terminator per expression.

---

## 4) `assign.l` / `assign.y` — Assignment with expression on RHS

Purpose
- Parse `ID = <expr>;` and print the computed value: e.g., `x = 9`.

Lexer highlights (`assign.l`)
- Tokens: `ID`, `NUM`, `FLOAT`, `ASSIGN` (`=`), `SEMICOLON`, operators `+ - * / % ^` and parentheses.
- When matching an `ID`, the lexer saves the lexeme into a global `char id_name[64]` so the parser can print it later.

Grammar and precedence (`assign.y`)
```
stmt → ID ASSIGN expr SEMICOLON   { prints as integer if integral, else %g }
expr → + - * / % ^ with precedence; unary minus; NUM and FLOAT literals
```

Behavior and examples
- `x = 3 * (2 + 1);` → `x = 9`
- `y = -4 + 6;` → `y = 2`

Limitations
- No symbol table: the assignment isn’t stored for future use.
- Missing `;` or malformed RHS triggers `yyerror`.

Key point to mention
- Quick hack of passing the identifier string from lexer to parser via a global; a more robust design uses `yylval` with a union and typed tokens.

---

## Quick viva Q&A

- How is operator precedence handled?
  - Via Bison precedence/associativity declarations: `%left`, `%right`, and `%prec` for unary minus.

- Why define `UMINUS`?
  - To control precedence and associativity of unary minus separately from binary `-`.

- What is `yywrap` and why not link `-lfl`?
  - `yywrap()` marks end-of-input. Defining it in the lexer avoids needing Flex’s runtime library on Windows.

- How do numbers reach the parser?
  - The lexer sets `yylval = atoi(yytext)` before returning `NUM`. In these grammars, `YYSTYPE` is `int`.

- How is the keyword `int` recognized in `decl.l`?
  - After matching an identifier, the lexer compares the lexeme to `"int"` and returns `INT` if equal; otherwise `ID`.

- How to extend `assign.y` to use variables on the RHS?
  - Add a symbol table (map from `string` → `int`), store values on assignment, and add a rule `expr → ID { $$ = lookup(id_name); }` with an error for undefined IDs.

---

## Demo snippets (optional during presentation)

- Expression evaluator
  ```powershell
  echo "3 + 4 * 5" | .\expr.exe
  ```

- Declaration validator
  ```powershell
  echo "int a, b, c;" | .\decl.exe
  ```

- Binary expression
  ```powershell
  echo "12 + 5" | .\binexpr.exe
  ```

- Assignment
  ```powershell
  echo "x = 3 * (2 + 1);" | .\assign.exe
  ```

---

## One-slide summary

- `expr`: full evaluator with precedence, unary minus, division-by-zero check
- `decl`: validates `int` declarations with a comma-separated list
- `binexpr`: exactly `NUM op NUM` per line; newline terminates
- `assign`: `ID = expr;` — prints computed value; no symbol table yet; supports % and ^; on div/mod-by-zero assigns 0

That’s all you need to explain and demo the lab clearly.
