%{ 
#include <stdio.h>
#include <string.h>
#include "y.tab.h"
%}

%%
[ \t\r\n]+           ;
"while"              { return WHILE; }
"<="                 { return LE; }
">="                 { return GE; }
"=="                 { return EQ; }
"!="                 { return NE; }
"<"                  { return LT; }
">"                  { return GT; }
[0-9]+                { yylval.str = strdup(yytext); return NUM; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return ID; }
"="                  { return '='; }
";"                  { return ';'; }
"("                  { return '('; }
")"                  { return ')'; }
"{"                  { return '{'; }
"}"                  { return '}'; }
"+"                  { return '+'; }
"-"                  { return '-'; }
"*"                  { return '*'; }
"/"                  { return '/'; }
.                     { printf("Unknown character: %s\n", yytext); }

%%

int yywrap(void) { return 1; }
