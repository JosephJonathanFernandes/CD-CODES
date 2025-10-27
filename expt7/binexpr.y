%{
#include <stdio.h>
#include <stdlib.h>
#define YYSTYPE int
int yylex(void);
void yyerror(const char *s);
%}

%token NUM

%%

input:
      /* empty */
    | input line
    ;

line:
      NUM '+' NUM '\n'    { printf("Parsed: %d + %d => Result = %d\n", $1, $3, $1+$3); }
    | NUM '-' NUM '\n'    { printf("Parsed: %d - %d => Result = %d\n", $1, $3, $1-$3); }
    | NUM '*' NUM '\n'    { printf("Parsed: %d * %d => Result = %d\n", $1, $3, $1*$3); }
    | NUM '/' NUM '\n'    { if($3==0) { printf("Error: division by zero\n"); } else printf("Parsed: %d / %d => Result = %d\n", $1, $3, $1/$3); }
    ;

%%

void yyerror(const char *s) { fprintf(stderr, "Invalid input\n"); }

int main(void) {
    printf("Enter binary expressions (num1 op num2). Ctrl+Z then Enter to quit.\n");
    yyparse();
    return 0;
}
