%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char *s);
%}

%token VOID CHAR SHORT INT LONG FLOAT DOUBLE SIGNED UNSIGNED
%token CONST VOLATILE TYPEDEF STATIC EXTERN REGISTER
%token ID NUMBER FLOATCONST CHARCONST STRINGLIT
%token COMMA SEMICOLON ASSIGN ASTERISK LBRACKET RBRACKET LPAREN RPAREN INVALID

%%

decl
    : decl_specifiers init_declarator_list SEMICOLON   { printf("Valid declaration\n"); }
    ;

/* declaration specifiers: storage class | type specifiers | type qualifiers */
decl_specifiers
    : decl_specifiers decl_specifier
    | decl_specifier
    ;

decl_specifier
    : storage_class_specifier
    | type_qualifier
    | type_token
    ;

storage_class_specifier
    : TYPEDEF
    | EXTERN
    | STATIC
    | REGISTER
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

type_qualifier
    : CONST
    | VOLATILE
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
    : ID
    | LPAREN declarator RPAREN
    | direct_declarator LBRACKET const_expr_opt RBRACKET
    | direct_declarator LPAREN parameter_list_opt RPAREN
    ;

const_expr_opt
    : /* empty */
    | NUMBER
    | ID
    ;

/* keep initializer simple (constants or identifiers) */
initializer
    : NUMBER
    | FLOATCONST
    | CHARCONST
    | STRINGLIT
    | ID
    ;

/* parameters: simplified */
parameter_list_opt
    : /* empty */
    | parameter_list
    ;

parameter_list
    : parameter_declaration
    | parameter_list COMMA parameter_declaration
    ;

parameter_declaration
    : decl_specifiers declarator
    | decl_specifiers
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
