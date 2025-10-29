%{
#include "assign.tab.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Helpers to process character and string literals */
static char unescape_char(const char *s) {
	if (s[0] != '\\') return s[0];
	switch (s[1]) {
		case 'n':  return '\n';
		case 't':  return '\t';
		case 'r':  return '\r';
		case '\\': return '\\';
		case '\'': return '\'';
		case '"': return '"';
		case '0': return '\0';
		default:   return s[1];
	}
}

static char *unquote_string(const char *text) {
	size_t len = strlen(text);
	if (len < 2) return strdup("");
	char *out = (char*)malloc(len - 1);
	size_t oi = 0;
	for (size_t i = 1; i + 1 < len; ++i) {
		if (text[i] == '\\' && i + 1 < len - 1) {
			out[oi++] = unescape_char(&text[i]);
			i++;
		} else {
			out[oi++] = text[i];
		}
	}
	out[oi] = '\0';
	return out;
}

int yywrap(void){ return 1; }
%}
%%

"true"|"false" { yylval.bval = (yytext[0] == 't'); return yytext[0] == 't' ? TRUE : FALSE; }
([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)? { yylval.fval = strtod(yytext, NULL); return FLOAT; }
[0-9]+([eE][+-]?[0-9]+)?      { yylval.ival = (int)strtol(yytext, NULL, 10); return NUM; }

\'.\' {
	/* single character (with simple escapes) */
	yylval.cval = yytext[1];
	return CHARLIT;
}
\"[^\"\n]*\" {
	yylval.sval = unquote_string(yytext);
	return STRING;
}
[a-zA-Z_][a-zA-Z0-9_]* { yylval.sval = strdup(yytext); return ID; }
"="        { return ASSIGN; }
";"        { return SEMICOLON; }
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }
"("        { return '('; }
")"        { return ')'; }
[ \t\n]+   ;
.           { return yytext[0]; }
%%
