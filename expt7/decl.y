%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char *s);
%}

%token VOID CHAR SHORT INT LONG FLOAT DOUBLE SIGNED UNSIGNED
%token ID NUMBER FLOATCONST CHARCONST COMMA SEMICOLON ASSIGN ASTERISK LBRACKET RBRACKET INVALID

%%

decl
    : type_specifier init_declarator_list SEMICOLON   { printf("Valid declaration\n"); }
    ;

/* one or more type tokens like: unsigned long long int */
type_specifier
    : type_token_list
    ;

type_token_list
    : type_token
    | type_token_list type_token
    ;

type_token
    : VOID
    | CHAR
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    | SIGNED
    | UNSIGNED
    ;

init_declarator_list
    : init_declarator
    | init_declarator_list COMMA init_declarator
    ;

init_declarator
    : declarator
    | declarator ASSIGN initializer
    ;

/* pointer and array declarators like: *p, **q, a[10], b[3][4] */
declarator
    : pointer_opt direct_declarator
    ;

pointer_opt
    : /* empty */
    | pointer
    ;

pointer
    : ASTERISK
    | ASTERISK pointer
    ;

direct_declarator
    : ID array_dim_opt
    ;

array_dim_opt
    : /* empty */
    | array_dim_opt LBRACKET const_number_opt RBRACKET
    ;

const_number_opt
    : /* empty */
    | NUMBER
    ;

/* keep initializer simple (constants or identifiers) */
initializer
    : NUMBER
    | FLOATCONST
    | CHARCONST
    | ID
    ;

%%
void yyerror(const char *s) {
    printf("Invalid declaration\n");
}

int main() {
    printf("Enter declaration: ");
    yyparse();
    return 0;
}
