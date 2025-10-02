%{
#include <stdio.h>
#include <string.h>
int lineno = 1;
char comment_buffer[1000];  // Buffer to store multi-line comments
%}

%x COMMENT

%%
("auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"phone"|"email"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while") { printf("<KEYWORD, %s>\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*   { printf("<IDENTIFIER, %s >\n", yytext); }

[0-9]+\.[0-9]+           { printf("<FLOAT, %s >\n", yytext); }
[0-9]+                   { printf("<INTEGER, %s >\n", yytext); }
\"([^"\n]|(\\.))*\"      { printf("<STRING, %s >\n", yytext); }
\'([^'\n]|(\\.))\'       { printf("<CHAR, %s >\n", yytext); }

(\+91-)?[0-9]{10}        { printf("<PHONE, %s >\n", yytext); }
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,} { printf("<EMAIL, %s >\n", yytext); }

"=="|"!="|"<="|">="|"="|"+"|"-"|"*"|"/"|">"|"<"   { printf("<OPERATOR, %s >\n", yytext); }
"{"|"}"|"("|")"|";"|","|"["|"]"                  { printf("<PUNCTUATOR, %s >\n", yytext); }

"//".*                    { printf("<SINGLE_LINE_COMMENT, %s>\n", yytext); }

"/*"                      { BEGIN(COMMENT); strcpy(comment_buffer, yytext); }
<COMMENT>"*/"             { strcat(comment_buffer, yytext); printf("<MULTI_LINE_COMMENT, %s>\n", comment_buffer); BEGIN(INITIAL); }
<COMMENT>\n               { strcat(comment_buffer, yytext); lineno++; }
<COMMENT>.                { strcat(comment_buffer, yytext); }

[ \t\r]+                 { /* Ignore whitespace (including CR) */ }
\n                      { lineno++; }
.                       { printf("ERROR: Unknown symbol '%s' at line %d\n", yytext, lineno); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
