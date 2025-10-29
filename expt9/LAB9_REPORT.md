# LAB SESSION 9: YACC — Intermediate Code Generation (TAC)

## Aim
Implement a YACC (Bison) program with a Flex lexer to generate three-address intermediate code (TAC) for arithmetic expressions, assignments, and while loops.

## Problem Definition
Design and implement a YACC program that can:
- Parse arithmetic expressions involving:
  - Integer constants and variables
  - Binary operators: `+`, `-`, `*`, `/`
  - Parentheses for grouping
- Parse while loops of the form:
  ```
  while (condition) {
      statements
  }
  ```
  where `condition` is a relational expression using `<, <=, >, >=, ==, !=`, and statements include assignments and nested arithmetic expressions.
- Generate Three-Address Code (TAC) for expressions and while loops.

## Theory (Brief)
Three-Address Code (TAC) represents computations using simple instructions with at most three operands, typically `x = y op z` or label/jump forms for control flow. It simplifies subsequent optimization and target code generation. Using syntax-directed translation with YACC, semantic actions attached to grammar rules emit TAC incrementally while parsing the input.

## Design and Approach
- Lexer (`lexer.l`):
  - Produces tokens: `ID`, `NUM`, `WHILE`, relational tokens `LT, LE, GT, GE, EQ, NE`, and single-char tokens for operators, `=`, delimiters, and braces.
  - Sets `yylval.str` to the string value for `ID` and `NUM`.
- Parser (`grammar.y`):
  - Operator precedence: `*`/`/` > `+`/`-`; unary minus has the highest precedence (`%right UMINUS`).
  - Expressions (`expr`): build TAC using temporaries `t1, t2, ...`.
  - Assignments: `id = expr;` becomes a direct move from the expression temporary to the variable.
  - Relational conditions (`cond`): `t = a relop b` where relop is one of `<, <=, >, >=, ==, !=`.
  - While loops: use labels `Lk` for loop start and exit.
    - Pattern:
      ```
      Lstart:
      tC = <relational condition>
      if tC == 0 goto Lexit
      ... body TAC ...
      goto Lstart
      Lexit:
      ```
    - Implemented with mid-rule actions to ensure the conditional branch is emitted immediately after parsing the condition, before the body.
  - Supports nested loops via separate start- and exit-label stacks.

## Build and Run
- Requirements: `bison`/`yacc`, `flex`/`lex`, `gcc`.
- Windows (PowerShell) commands:
  ```powershell
  bison -d -y grammar.y
  flex lexer.l
  gcc -o tac y.tab.c lex.yy.c
  # Run with a file
  Get-Content test1.txt | .\tac.exe
  ```
  Notes: On Windows/MinGW we don’t link `-lfl` because `yywrap` is provided in `lexer.l`.

## Source Listings (Key Parts)
- Grammar: see `grammar.y` — contains semantic actions `emit(...)`, temporary/label generators, and while-loop mid-rule actions for correct control flow.
- Lexer: see `lexer.l` — tokenization rules, returns relational tokens and identifiers/numbers with attached strings.

## TAC Format Emitted
- Expression: `tX = y op z` or `tX = - y`
- Assignment: `x = y`
- Labels: printed as `Lk:`
- Conditional jump: `if t == 0 goto Lk`
- Unconditional jump: `goto Lk`

## Test Suite and Results
Executed on 2025-10-30 using PowerShell; each input piped to `tac.exe`.

1) tests/t01_assign.txt
```
x = 42;
```
Output:
```
x = 42
```

2) tests/t02_prec.txt
```
x = 1 + 2 * 3;
```
Output:
```
t1 = 2 * 3
`t2 = 1 + t1`
x = t2
```

3) tests/t03_paren.txt
```
x = (1 + 2) * 3;
```
Output:
```
t1 = 1 + 2
`t2 = t1 * 3`
x = t2
```

4) tests/t04_unary.txt
```
a = 10;
x = -a;
y = - ( -5 );
```
Output:
```
a = 10
`t1 = - a`
x = t1
`t2 = - 5`
`t3 = - t2`
y = t3
```

5) tests/t05_div_sub.txt
```
a = 10;
b = 6;
c = 2;
z = a - b / c;
```
Output:
```
a = 10
b = 6
c = 2
`t1 = b / c`
`t2 = a - t1`
z = t2
```

6) tests/t06_while_lt.txt
```
i = 0;
while (i < 3) {
    i = i + 1;
}
```
Output:
```
i = 0
L1:
`t1 = i < 3`
`if t1 == 0 goto L2`
`t2 = i + 1`
i = t2
`goto L1`
L2:
```

7) tests/t07_while_le_expr.txt
```
i = 0;
sum = 0;
while (i <= 4) {
    sum = sum + i * 2;
    i = i + 2;
}
```
Output:
```
i = 0
sum = 0
L1:
`t1 = i <= 4`
`if t1 == 0 goto L2`
`t2 = i * 2`
`t3 = sum + t2`
sum = t3
`t4 = i + 2`
i = t4
`goto L1`
L2:
```

8) tests/t08_while_gt.txt
```
n = 3;
while (n > 0) {
    n = n - 1;
}
```
Output:
```
n = 3
L1:
`t1 = n > 0`
`if t1 == 0 goto L2`
`t2 = n - 1`
n = t2
`goto L1`
L2:
```

9) tests/t09_while_ge_complex.txt
```
a = 5;
b = 0;
while (a + b >= 5) {
    a = a - 1;
}
```
Output:
```
a = 5
b = 0
L1:
`t1 = a + b`
`t2 = t1 >= 5`
`if t2 == 0 goto L2`
`t3 = a - 1`
a = t3
`goto L1`
L2:
```

10) tests/t10_while_eq.txt
```
x = 0;
y = 0;
while (x == y) {
    x = x + 1;
}
```
Output:
```
x = 0
y = 0
L1:
`t1 = x == y`
`if t1 == 0 goto L2`
`t2 = x + 1`
x = t2
`goto L1`
L2:
```

11) tests/t11_while_ne.txt
```
x = 5;
while (x != 0) {
    x = x / 2;
}
```
Output:
```
x = 5
L1:
`t1 = x != 0`
`if t1 == 0 goto L2`
`t2 = x / 2`
x = t2
`goto L1`
L2:
```

12) tests/t12_nested_while.txt
```
i = 0;
j = 0;
while (i < 3) {
    while (j < 2) {
        j = j + 1;
    }
    i = i + 1;
    j = 0;
}
```
Output:
```
i = 0
j = 0
L1:
`t1 = i < 3`
`if t1 == 0 goto L2`
L3:
`t2 = j < 2`
`if t2 == 0 goto L4`
`t3 = j + 1`
j = t3
`goto L3`
L4:
`t4 = i + 1`
i = t4
j = 0
`goto L1`
L2:
```

## Quality Gates
- Build: PASS (bison/flex/gcc on Windows via MinGW; linked without `-lfl`)
- Run: PASS (all 12 tests executed; TAC output matches expectations)
- Lint/Typecheck: N/A (C is compiled by GCC; no warnings observed at default settings)

## Conclusion
The implemented YACC+Flex program meets the problem requirements:
- Parses integer expressions with correct precedence, parentheses, and unary minus.
- Parses while loops with relational conditions using `<, <=, >, >=, ==, !=`.
- Generates correct Three-Address Code (TAC) for expressions, assignments, and while loops, including nested loops, using labels and conditional/unconditional jumps.

## Possible Extensions
- Support `if`/`else`, `break`/`continue`, and logical `&&`/`||` with short-circuiting.
- Emit quadruple form and store TAC in a data structure for optimization passes.
- Add a symbol table with basic semantic checks and constant folding.
