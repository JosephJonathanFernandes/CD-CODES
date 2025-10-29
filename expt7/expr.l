%{
#include "expr.tab.h"
#include <stdlib.h>

/* yylval is defined by bison/yacc as an int (see expr.y) */

/* Provide yywrap so linking doesn't require -lfl on Windows/mingw */
int yywrap(void) { return 1; }
%}

%%
[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?  { yylval = strtod(yytext, NULL); return NUM; }
\.[0-9]+([eE][+-]?[0-9]+)?           { yylval = strtod(yytext, NULL); return NUM; }
[ \t]+     ;
"\n"      { return '\n'; }
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }
"("        { return '('; }
")"        { return ')'; }
.           { return yytext[0]; }
%%
