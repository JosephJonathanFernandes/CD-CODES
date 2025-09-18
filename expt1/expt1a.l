%{
#include <stdio.h>
int yylex(void);
int yywrap(void);
%}

%%
[0-9]+                { printf("%s is an INTEGER\n", yytext); }
[0-9]+"."[0-9]+       { printf("%s is a REAL NUMBER\n", yytext); }
[a-zA-Z]+             { printf("%s is a WORD\n", yytext); }
.|\n                  { /* ignore other characters */ }
%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
