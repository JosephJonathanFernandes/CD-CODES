%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern int yylineno;
void yyerror(const char *s);
%}

%union {
  char *s;
}

%token <s> ID NUM
%token INC DEC
%token LE GE EQ NE
%token FOR WHILE DO
%token TYPE

%left '+' '-'
%left '*' '/'
%right UMINUS

%start program

%%

program:
    stmt_list
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
    expr '+' expr
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
    expr relop expr
  ;

relop:
    '<' | '>' | LE | GE | EQ | NE
  ;

for_inc:
    ID INC
  | ID DEC
  | assignment
  ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error at line %d: %s\n", yylineno, s);
}

int main(void) {
    if (yyparse() == 0) {
        printf("Input is syntactically correct.\n");
        return 0;
    } else {
        printf("Input has syntax errors.\n");
        return 1;
    }
}
