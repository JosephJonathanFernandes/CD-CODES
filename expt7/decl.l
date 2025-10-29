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
	return ID;
}
","             { return COMMA; }
";"             { return SEMICOLON; }
"="             { return ASSIGN; }
"*"             { return ASTERISK; }
"["             { return LBRACKET; }
"]"             { return RBRACKET; }

[0-9]+           { return NUMBER; }

[ \t\n\r]+     { /* skip whitespace */ }
.               { return INVALID; }
%%
