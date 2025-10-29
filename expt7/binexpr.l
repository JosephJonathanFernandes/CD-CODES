%{
#include "binexpr.tab.h"
#include <stdlib.h>
int yywrap(void){ return 1; }
%}

%%
[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?  { yylval = strtod(yytext, NULL); return NUM; }
[ \t]+     ;
"\r\n"   { return '\n'; }
"\n"      { return '\n'; }
"\r"      ;
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }
"%"        { return '%'; }
"^"        { return '^'; }
.           { return yytext[0]; }
%%
