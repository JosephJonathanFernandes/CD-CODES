%{
#include <stdio.h>
#include <string.h>
int lineno = 1;
%}

%%
"int"|"float"|"char"|"if"|"else"|"while"|"for"|"return"|"phone"|"email"
    { printf("<KEYWORD, %s>\n", yytext); }



[a-zA-Z_][a-zA-Z0-9_]*   { printf("<IDENTIFIER, %s>\n", yytext); }


[0-9]+                   { printf("<INTEGER, %s>\n", yytext); }
[0-9]+"."[0-9]+          { printf("<FLOAT, %s>\n", yytext); }
\"([^"\n]|(\\.))*\"      { printf("<STRING, %s>\n", yytext); }
\'([^'\n]|(\\.))\'       { printf("<CHAR, %s>\n", yytext); }

(\+91-)?[0-9]{10}        { printf("<PHONE, %s>\n", yytext); }
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}  { printf("<EMAIL, %s>\n", yytext); }


"=="|"!="|"<="|">="|"="|"+"|"-"|"*"|"/"   { printf("<OPERATOR, %s>\n", yytext); }
"{"|"}"|"("|")"|";"|","                  { printf("<PUNCTUATOR, %s>\n", yytext); }


"//".*                  { /* Ignore single-line */ }
"/*"([^*]|\n)*"*/"      { /* Ignore multi-line */ }


[ \t]+                  ;
\n                      { lineno++; }


.                       { printf("ERROR: Unknown symbol '%s' at line %d\n", yytext, lineno); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
