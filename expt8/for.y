%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern int yylineno;
void yyerror(const char *s);
int had_error = 0; /* flag for current program */
%}

%union {
  char *s;
}

%token <s> ID NUM
%token INC DEC
%token LE GE EQ NE
%token FOR WHILE DO
%token TYPE
%token SEP

%left EQ NE
%left '<' '>' LE GE
%left '+' '-'
%left '*' '/'
%right UMINUS

%start program_list

%%

program_list:
    /* empty */
  | program_list program
  ;

program:
    stmt_list SEP   { if (!had_error) printf("Program: syntactically correct.\n"); else printf("Program: has syntax errors.\n"); had_error = 0; }
  | stmt_list      { /* last program may not have trailing SEP */ if (!had_error) printf("Program: syntactically correct.\n"); else printf("Program: has syntax errors.\n"); had_error = 0; }
  | error SEP      { printf("Program: has syntax errors.\n"); yyclearin; had_error = 0; }
  ;

stmt_list:
    /* empty */
  | stmt_list stmt
  ;

stmt:
    assignment ';'
  | decl_stmt
  | for_stmt
  | while_stmt
  | do_while_stmt
  | block
  ;

block:
    '{' stmt_list '}'
  ;

assignment:
    ID '=' expr      { /* assignment accepted */ }
  ;

decl_stmt:
    TYPE ID ';'
  | TYPE ID '=' expr ';'
  ;

expr:
    expr '<' expr
  | expr '>' expr
  | expr LE expr
  | expr GE expr
  | expr EQ expr
  | expr NE expr
  | expr '+' expr
  | expr '-' expr
  | expr '*' expr
  | expr '/' expr
  | '-' expr %prec UMINUS
  | '(' expr ')'
  | ID
  | NUM
  ;

for_stmt:
    FOR '(' for_init ';' for_cond ';' for_inc ')' stmt
  ;

while_stmt:
    WHILE '(' expr ')' stmt
  ;

do_while_stmt:
    DO stmt WHILE '(' expr ')' ';'
  ;

for_init:
    assignment
  ;

for_cond:
    expr
  ;

for_inc:
    ID INC
  | ID DEC
  | assignment
  ;

%%

void yyerror(const char *s) {
  fprintf(stderr, "Syntax error at line %d: %s\n", yylineno, s);
  had_error = 1;
}

int main(void) {
  /* parse input and rely on per-program messages; return 0 */
  yyparse();
  return 0;
}
