%{
#include "decl.tab.h"
#include <stdlib.h>
#include <string.h>
int yywrap(void){ return 1; }
%}


%%
[a-zA-Z_][a-zA-Z0-9_]*    {
	/* Keywords for basic and modifier types */
	if (strcmp(yytext, "int") == 0) return INT;
	if (strcmp(yytext, "float") == 0) return FLOAT;
	if (strcmp(yytext, "double") == 0) return DOUBLE;
	if (strcmp(yytext, "char") == 0) return CHAR;
	if (strcmp(yytext, "short") == 0) return SHORT;
	if (strcmp(yytext, "long") == 0) return LONG;
	if (strcmp(yytext, "signed") == 0) return SIGNED;
	if (strcmp(yytext, "unsigned") == 0) return UNSIGNED;
	if (strcmp(yytext, "void") == 0) return VOID;
	if (strcmp(yytext, "const") == 0) return CONST;
	if (strcmp(yytext, "volatile") == 0) return VOLATILE;
	if (strcmp(yytext, "typedef") == 0) return TYPEDEF;
	if (strcmp(yytext, "static") == 0) return STATIC;
	if (strcmp(yytext, "extern") == 0) return EXTERN;
	if (strcmp(yytext, "register") == 0) return REGISTER;
	return ID;
}
","             { return COMMA; }
";"             { return SEMICOLON; }
"="             { return ASSIGN; }
"*"             { return ASTERISK; }
"["             { return LBRACKET; }
"]"             { return RBRACKET; }
"("             { return LPAREN; }
")"             { return RPAREN; }
	[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?   { return FLOATCONST; }
	\.[0-9]+([eE][+-]?[0-9]+)?         { return FLOATCONST; }
	[0-9]+([eE][+-]?[0-9]+)             { return FLOATCONST; }

[0-9]+                              { return NUMBER; }

	\"([^\\\"\n]|\\.)*\"            { return STRINGLIT; }
'(\\.|[^\\\n])'                { return CHARCONST; }

[ \t\n\r]+     { /* skip whitespace */ }
.               { return INVALID; }
%%
