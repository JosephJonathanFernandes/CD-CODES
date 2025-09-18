%{
#include <stdio.h>
#include <string.h>

int keyword_count = 0, id_count = 0, const_count = 0, op_count = 0;
char *keywords[] = {"int", "float", "return", "if", "else", "while", "for", "char", "double"};

int is_keyword(char *str) {
    for (int i = 0; i < sizeof(keywords)/sizeof(keywords[0]); i++)
        if (strcmp(str, keywords[i]) == 0) return 1;
    return 0;
}
%}

%%

[0-9]+(\.[0-9]+)?        { const_count++; }
[a-zA-Z_][a-zA-Z0-9_]*   {
                            if (is_keyword(yytext)) keyword_count++;
                            else id_count++;
                         }
[+\-*/=<>!]+             { op_count++; }
[ \t\n]                  { /* ignore whitespace */ }
.                        { /* ignore other chars */ }

%%

int yywrap() { return 1; }

int main() {
    yylex();
    printf("Keywords: %d\nIdentifiers: %d\nConstants: %d\nOperators: %d\n", 
            keyword_count, id_count, const_count, op_count);
    return 0;
}

