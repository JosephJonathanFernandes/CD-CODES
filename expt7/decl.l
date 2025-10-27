%{
#include "decl.tab.h"
#include <stdlib.h>
int yywrap(void){ return 1; }
%}

%%
int\b     { return INT; }
[a-zA-Z][a-zA-Z0-9]*    { return ID; }","     { return COMMA; }
";"     { return SEMICOLON; }
[ \t\n]+ ;     // ignore whitespace
.       { return INVALID; }
%%
