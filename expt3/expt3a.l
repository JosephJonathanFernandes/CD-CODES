%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAXWORDS 1000

struct {
    char word[50];
    int count;
} table[MAXWORDS];

int nwords = 0;

void insert_word(char *w) {
    for (int i = 0; i < nwords; i++) {
        if (strcmp(table[i].word, w) == 0) {
            table[i].count++;
            return;
        }
    }
    strcpy(table[nwords].word, w);
    table[nwords].count = 1;
    nwords++;
}

%}

%%
[a-zA-Z]+   { 
                char temp[50]; 
                int i;
                for(i=0; yytext[i]; i++) 
                    temp[i] = tolower(yytext[i]);
                temp[i] = '\0';
                insert_word(temp);
            }

[0-9]+              ;   /* ignore numbers */
[ \t\n\r.,;:!?\"\'()-]+   ;   /* ignore punctuation/whitespace */
.                   ;   /* ignore other characters */
%%

int cmp(const void *a, const void *b) {
    return strcmp(((struct {char word[50]; int count;}*)a)->word,
                  ((struct {char word[50]; int count;}*)b)->word);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <inputfile>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        printf("Could not open file %s\n", argv[1]);
        return 1;
    }

    yyin = fp;
    yylex();
    fclose(fp);

    qsort(table, nwords, sizeof(table[0]), cmp);

    printf("\nWord Frequency Analysis:\n");
    for (int i = 0; i < nwords; i++) {
        printf("%s : %d\n", table[i].word, table[i].count);
    }

    return 0;
}

int yywrap() {
    return 1;
}
