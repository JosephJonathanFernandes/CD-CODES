%{
#include "for.tab.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* yylval is a union; set the string field */
extern int yylineno;
%}

%%
"for"               { return FOR; }
"while"            { return WHILE; }
"do"               { return DO; }
"int"              { yylval.s = strdup(yytext); return TYPE; }
"++"                { return INC; }
"--"                { return DEC; }
"<="                { return LE; }
">="                { return GE; }
"=="                { return EQ; }
"!="                { return NE; }
";"                 { return ';'; }
"("                 { return '('; }
")"                 { return ')'; }
"{"                 { return '{'; }
"}"                 { return '}'; }
"="                 { return '='; }
"+"                 { return '+'; }
"-"                 { return '-'; }
[ \t\r]+            { /* skip spaces/tabs */ }
"\n"                { yylineno++; }
[0-9]+              { yylval.s = strdup(yytext); return NUM; }
[A-Za-z_][A-Za-z0-9_]* { yylval.s = strdup(yytext); return ID; }
.                   { return yytext[0]; }

%%

int yywrap(void) { return 1; }
