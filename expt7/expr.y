%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);

/* Track whether the current input line had an error (syntax or semantic) */
static int had_error_line = 0;
%}

%define api.value.type {double}

%token NUM
%left '+' '-'
%left '*' '/'
%right UMINUS

%%

input:
            /* empty */
        | input line
        ;

line:
            expr '\n'    { if (!had_error_line) printf("Result = %g\n", $1); had_error_line = 0; }
        | error '\n'   { had_error_line = 0; yyerrok; }
        ;

expr:
            expr '+' expr    { $$ = $1 + $3; }
        | expr '-' expr    { $$ = $1 - $3; }
        | expr '*' expr    { $$ = $1 * $3; }
        | expr '/' expr    { if ($3 == 0.0) { yyerror("division by zero"); $$ = 0.0; } else $$ = $1 / $3; }
        | '-' expr %prec UMINUS { $$ = -$2; }
        | '(' expr ')'     { $$ = $2; }
        | NUM              { $$ = $1; }
        ;

%%

void yyerror(const char *s) {
    had_error_line = 1;
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Enter expression (press Ctrl+Z then Enter to quit on Windows)\n");
    yyparse();
    return 0;
}
