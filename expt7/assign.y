%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int yylex(void);
void yyerror(const char *s);
%}

%union {
    int    ival;
    double fval;
    char   cval;
    int    bval;   /* 0/1 for false/true */
    char  *sval;   /* for ID and STRING */
}

%token <sval> ID
%token <ival> NUM
%token <fval> FLOAT
%token <cval> CHARLIT
%token <sval> STRING
%token <bval> TRUE FALSE
%token ASSIGN SEMICOLON

%type <fval> expr

%left '+' '-'
%left '*' '/'
%right UMINUS

%%

input:
            /* empty */
        | input stmt
        ;

stmt:
            ID ASSIGN expr SEMICOLON     {
                                                                            /* Print numeric result; avoid trailing .0 when integer */
                                                                            if (fabs($3 - (long long)$3) < 1e-9) printf("%s = %lld\n", $1, (long long)$3);
                                                                            else printf("%s = %g\n", $1, $3);
                                                                            free($1);
                                                                        }
        | ID ASSIGN CHARLIT SEMICOLON  { printf("%s = '%c'\n", $1, $3); free($1); }
        | ID ASSIGN STRING SEMICOLON   { printf("%s = \"%s\"\n", $1, $3); free($1); free($3); }
        | ID ASSIGN TRUE SEMICOLON     { printf("%s = true\n", $1); free($1); }
        | ID ASSIGN FALSE SEMICOLON    { printf("%s = false\n", $1); free($1); }
        ;

expr:
            expr '+' expr    { $$ = $1 + $3; }
        | expr '-' expr    { $$ = $1 - $3; }
        | expr '*' expr    { $$ = $1 * $3; }
        | expr '/' expr    { if (fabs($3) < 1e-12) { yyerror("division by zero"); $$ = 0.0; } else $$ = $1 / $3; }
        | '-' expr %prec UMINUS { $$ = -$2; }
        | '(' expr ')'     { $$ = $2; }
        | NUM              { $$ = (double)$1; }
        | FLOAT            { $$ = $1; }
        ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Enter assignments like: x = 3 + 4; y = 3.14; c = 'A'; s = \"hi\"; b = true;\n");
    printf("Ctrl+Z then Enter to quit.\n");
    yyparse();
    return 0;
}
