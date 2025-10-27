%{
#include <stdio.h>
%}

%%
[0-9]+   { printf("NUMBER: %s\n", yytext); }
[a-zA-Z]+ { printf("WORD: %s\n", yytext); }
\n        { /* ignore newlines */ }
.         { printf("UNKNOWN: %s\n", yytext); }
%%

int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
