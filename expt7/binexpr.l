%{
#include "binexpr.tab.h"
#include <stdlib.h>
int yywrap(void){ return 1; }
%}

%%
[0-9]+      { yylval = atoi(yytext); return NUM; }
[ \t]+     ;
"\n"      { return '\n'; }
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }
.           { return yytext[0]; }
%%
