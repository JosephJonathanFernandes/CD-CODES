%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int yylex(void);
void yyerror(const char *s);

/* Print helper: show integer without .0, otherwise compact float */
static void print_num(double v) {
  long long iv = (long long)v;
  if (v == (double)iv) {
    printf("%lld", iv);
  } else {
    printf("%g", v);
  }
}
%}

%define api.value.type {double}

%token NUM

%%

input:
      /* empty */
    | input line
    ;

line:
      NUM '+' NUM '\n'    { double r = $1 + $3; printf("Parsed: "); print_num($1); printf(" + "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); }
    | NUM '-' NUM '\n'    { double r = $1 - $3; printf("Parsed: "); print_num($1); printf(" - "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); }
    | NUM '*' NUM '\n'    { double r = $1 * $3; printf("Parsed: "); print_num($1); printf(" * "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); }
    | NUM '/' NUM '\n'    { if($3==0.0) { printf("Error: division by zero\n"); } else { double r = $1 / $3; printf("Parsed: "); print_num($1); printf(" / "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); } }
  | NUM '%' NUM '\n'    { if($3==0.0) { printf("Error: modulo by zero\n"); } else { double r = fmod($1, $3); printf("Parsed: "); print_num($1); printf(" %% "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); } }
    | NUM '^' NUM '\n'    { double r = pow($1, $3); printf("Parsed: "); print_num($1); printf(" ^ "); print_num($3); printf(" => Result = "); print_num(r); printf("\n"); }
    ;

%%

void yyerror(const char *s) { fprintf(stderr, "Invalid input\n"); }

int main(void) {
    printf("Enter binary expressions (num1 op num2). Ctrl+Z then Enter to quit.\n");
    yyparse();
    return 0;
}
