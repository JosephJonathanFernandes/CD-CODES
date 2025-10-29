%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

/* Track whether the current input line had an error (syntax or semantic) */
static int had_error_line = 0;

/* Simple symbol table for identifiers */
#define MAXSYMS 1024
#define NAMELEN 63
typedef struct { int in_use; char name[NAMELEN+1]; double val; } Sym;
static Sym syms[MAXSYMS];

int lookup(const char* name) {
    for (int i = 0; i < MAXSYMS; ++i) {
        if (syms[i].in_use && strcmp(syms[i].name, name) == 0) return i;
    }
    for (int i = 0; i < MAXSYMS; ++i) {
        if (!syms[i].in_use) {
            syms[i].in_use = 1;
            strncpy(syms[i].name, name, NAMELEN);
            syms[i].name[NAMELEN] = '\0';
            syms[i].val = 0.0;
            return i;
        }
    }
    yyerror("symbol table full");
    return 0;
}
%}

%union { double d; int sym; }

%token <d> NUM
%token <sym> ID
%token INC DEC
%left '+' '-'
%left '*' '/'
%right UMINUS

%type <d> expr

%%

input:
            /* empty */
        | input line
        ;

line:
            expr '\n'           { if (!had_error_line) printf("Result = %g\n", $1); had_error_line = 0; }
        | ID '=' expr '\n'    { if (!had_error_line) { syms[$1].val = $3; printf("%s = %g\n", syms[$1].name, syms[$1].val); } had_error_line = 0; }
        | error '\n'          { had_error_line = 0; yyerrok; }
        ;

expr:
            expr '+' expr    { $$ = $1 + $3; }
        | expr '-' expr    { $$ = $1 - $3; }
        | expr '*' expr    { $$ = $1 * $3; }
        | expr '/' expr    { if ($3 == 0.0) { yyerror("division by zero"); $$ = 0.0; } else $$ = $1 / $3; }
        | '-' expr %prec UMINUS { $$ = -$2; }
        | '(' expr ')'     { $$ = $2; }
        | NUM              { $$ = $1; }
        | ID               { $$ = syms[$1].val; }
        | INC ID           { syms[$2].val += 1.0; $$ = syms[$2].val; }  /* ++x */
        | DEC ID           { syms[$2].val -= 1.0; $$ = syms[$2].val; }  /* --x */
        | ID INC           { $$ = syms[$1].val; syms[$1].val += 1.0; }  /* x++ */
        | ID DEC           { $$ = syms[$1].val; syms[$1].val -= 1.0; }  /* x-- */
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
