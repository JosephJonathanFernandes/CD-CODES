# Strict Binary Expression (`binexpr.y`) and Lexer (`binexpr.l`) — Explained

This example enforces exactly two operands with one operator per input line. It’s useful to demonstrate precise pattern matching with Bison.

---

## What it does

- Accepts only lines of the form: `NUM op NUM` followed by a newline (`\n`).
- Supported ops: `+  -  *  /`.
- Prints the parsed form and result; handles division by zero gracefully.

Example
```text
Input:  12 + 5\n
Output: Parsed: 12 + 5 => Result = 17
```

---

## How the pieces talk

- `main()` in `binexpr.y` calls `yyparse()`.
- The parser repeatedly calls the lexer `yylex()` for tokens: `NUM`, operators, and newline `\n`.
- Each valid line must end with a newline to match a grammar rule and trigger output.

---

## Inside the parser: `binexpr.y`

Header contracts
```c
#define YYSTYPE int
int yylex(void);
void yyerror(const char *s);
```

Tokens
```bison
%token NUM
```

Grammar and actions
```bison
input: /* empty */ | input line ;

line:  NUM '+' NUM '\n'  { printf("Parsed: %d + %d => Result = %d\n", $1, $3, $1+$3); }
     | NUM '-' NUM '\n'  { printf("Parsed: %d - %d => Result = %d\n", $1, $3, $1-$3); }
     | NUM '*' NUM '\n'  { printf("Parsed: %d * %d => Result = %d\n", $1, $3, $1*$3); }
     | NUM '/' NUM '\n'  { if ($3==0) printf("Error: division by zero\n"); else printf("Parsed: %d / %d => Result = %d\n", $1, $3, $1/$3); }
     ;
```
- No general expression grammar here: only the four exact patterns are allowed.
- Newline (`'\n'`) is part of the rule; without it the line doesn’t match.

Error handling
```c
void yyerror(const char *s) { fprintf(stderr, "Invalid input\n"); }
```

---

## Inside the lexer: `binexpr.l`

Core rules (conceptual)
```flex
[0-9]+   { yylval = atoi(yytext); return NUM; }
[ \t]+  ;                // skip spaces/tabs
"\n"    { return '\n'; }
"+"|"-"|"*"|"/" { return yytext[0]; }
.       { return yytext[0]; }
int yywrap(void){ return 1; }
```
- Supplies numbers, operators, and the newline token to the parser.
- Anything else will be returned as its character and won’t match the strict grammar, causing an error.

---

## Examples

- `12 + 5\n` → `Parsed: 12 + 5 => Result = 17`
- `7 / 0\n` → `Error: division by zero`
- `3 + 4 + 5\n` → Invalid (doesn’t match any rule)

---

## Build and run (PowerShell)

```powershell
bison -d binexpr.y
flex binexpr.l
gcc lex.yy.c binexpr.tab.c -o binexpr.exe
.\binexpr.exe
# Example
# echo "12 + 5" | .\binexpr.exe
```

Notes
- Each input must end in a newline to trigger a `line` rule.
- No `-lfl` needed because `yywrap()` is defined in the lexer.

---

## Pitfalls and extensions

Pitfalls
- Inputs like `3 + 4 * 5` or `(3 + 4)` are invalid here by design.
- Missing newline won’t trigger evaluation.

Extensions
- Generalize to a full expression grammar with precedence (see `expr.y`).
- Add whitespace-tolerant syntax around operands and operator.
- Add error recovery to skip to next newline on invalid input.
