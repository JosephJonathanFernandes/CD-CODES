%{
#include <stdio.h>
#include <string.h>
int lineno = 1;
%}

%x COMMENT

%%
("auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while") { printf("<KEYWORD, %s>\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*   { printf("<IDENTIFIER, %s>\n", yytext); }

[0-9]+\.[0-9]+           { printf("<FLOAT, %s>\n", yytext); }
[0-9]+                   { printf("<INTEGER, %s>\n", yytext); }
\"([^"\n]|(\\.))*\"      { printf("<STRING, %s>\n", yytext); }
\'([^'\n]|(\\.))\'       { printf("<CHAR, %s>\n", yytext); }

(\+91-)?[0-9]{10}        { printf("<PHONE, %s>\n", yytext); }
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,} { printf("<EMAIL, %s>\n", yytext); }

"=="|"!="|"<="|">="|"="|"+"|"-"|"*"|"/"   { printf("<OPERATOR, %s>\n", yytext); }
"{"|"}"|"("|")"|";"|","                  { printf("<PUNCTUATOR, %s>\n", yytext); }

"//".*                    { /* Ignore single-line comments */ }

"/*"                      { BEGIN(COMMENT); }
<COMMENT>"*/"             { BEGIN(INITIAL); }
<COMMENT>\n               { lineno++; }
<COMMENT>.                { /* Ignore inside comment */ }

[ \t\r]+                 { /* Ignore whitespace (including CR) */ }
\n                      { lineno++; }
.                       { printf("ERROR: Unknown symbol '%s' at line %d\n", yytext, lineno); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
