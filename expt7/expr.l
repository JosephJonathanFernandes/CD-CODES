%{
#include "expr.tab.h"
#include <stdlib.h>
int lookup(const char* name);

/* yylval is a union declared by Bison in expr.y */

/* Provide yywrap so linking doesn't require -lfl on Windows/mingw */
int yywrap(void) { return 1; }
%}

%%
[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?  { yylval.d = strtod(yytext, NULL); return NUM; }
\.[0-9]+([eE][+-]?[0-9]+)?           { yylval.d = strtod(yytext, NULL); return NUM; }
"++"      { return INC; }
"--"      { return DEC; }
[A-Za-z_][A-Za-z0-9_]* { yylval.sym = lookup(yytext); return ID; }
[ \t]+     ;
"\n"      { return '\n'; }
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }
"%"        { return '%'; }
"^"        { return '^'; }
"="        { return '='; }
"("        { return '('; }
")"        { return ')'; }
.           { return yytext[0]; }
%%
