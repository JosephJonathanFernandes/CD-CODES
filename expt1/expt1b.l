%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
int yywrap(void);
%}

%%
[0-9]+  { 
    int num = atoi(yytext);
    int n = num;
    char hex[32];
    int i = 0;
    printf("Decimal: %d\n", num);
    if (num == 0) {
        printf("Step 1: %d / 16 = 0, remainder = 0\n", num);
        printf("Hexadecimal: 0\n");
    } else {
        while (n > 0) {
            int rem = n % 16;
            printf("Step %d: %d / 16 = %d, remainder = %d", i+1, n, n/16, rem);
            if (rem >= 10)
                printf(" ('%c')", 'A' + (rem - 10));
            printf("\n");
            hex[i++] = (rem < 10) ? ('0' + rem) : ('A' + (rem - 10));
            n /= 16;
        }
        printf("Hexadecimal: ");
        for (int j = i - 1; j >= 0; j--) putchar(hex[j]);
        printf("\n");
    }
}
.|\n    ;
%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
