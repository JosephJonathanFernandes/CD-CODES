%{
#include <stdio.h>
int yylex(void);
int yywrap(void);
int lineno = 1;
%}

%%
.*\n    { printf("%d: %s", lineno++, yytext); }
.       { printf("%d: %s", lineno++, yytext); }
%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
