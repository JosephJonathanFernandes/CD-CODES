# LEX Programming Guide: Complete Reference for Lexical Analysis

## Table of Contents
1. [Introduction to LEX](#introduction-to-lex)
2. [Lexical Analysis Fundamentals](#lexical-analysis-fundamentals)
3. [LEX Syntax and Structure](#lex-syntax-and-structure)
4. [Regular Expressions in LEX](#regular-expressions-in-lex)
5. [Advanced LEX Features](#advanced-lex-features)
6. [Integration with C Programming](#integration-with-c-programming)
7. [Common Patterns and Examples](#common-patterns-and-examples)
8. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
9. [Best Practices](#best-practices)
10. [Real-World Applications](#real-world-applications)

---

## Introduction to LEX

### What is LEX?
**LEX** (Lexical Analyzer Generator) is a powerful tool for generating lexical analyzers (scanners) that break down input text into tokens. It's an essential component in compiler construction and text processing applications.

### Key Features:
- **Pattern Matching**: Uses regular expressions to identify tokens
- **Action Execution**: Executes C code when patterns match
- **Automatic Code Generation**: Creates C source code for lexical analysis
- **Flexible Integration**: Seamlessly integrates with C programs
- **Efficient Processing**: Generates optimized finite state machines

### LEX vs. Other Tools:
| Tool | Purpose | Language | Output |
|------|---------|----------|---------|
| LEX | Lexical Analysis | C | C Source Code |
| FLEX | Enhanced LEX | C/C++ | C/C++ Source |
| ANTLR | Complete Parser | Java/C#/Python | Multiple Languages |
| JavaCC | Parser Generator | Java | Java Source |

---

## Lexical Analysis Fundamentals

### What is Lexical Analysis?
Lexical analysis is the **first phase** of compilation that converts a stream of characters into a stream of tokens. It's also called **scanning**.

### Process Overview:
```
Source Code → Lexical Analyzer → Token Stream → Parser
```

#### Input:
```c
int count = 42;
```

#### Output (Tokens):
```
<KEYWORD, int>
<IDENTIFIER, count>
<OPERATOR, =>
<INTEGER, 42>
<PUNCTUATOR, ;>
```

### Key Concepts:

#### 1. **Tokens**
Fundamental units of meaning in a programming language.
- **Keywords**: `int`, `if`, `while`, `return`
- **Identifiers**: Variable and function names
- **Literals**: Numbers, strings, characters
- **Operators**: `+`, `-`, `==`, `!=`
- **Punctuators**: `{`, `}`, `;`, `,`

#### 2. **Lexemes**
The actual character sequences that form tokens.
```
Token: INTEGER, Lexeme: "42"
Token: IDENTIFIER, Lexeme: "count"
```

#### 3. **Patterns**
Rules (regular expressions) that describe valid lexemes.
```
Integer Pattern: [0-9]+
Identifier Pattern: [a-zA-Z_][a-zA-Z0-9_]*
```

### Finite State Machines
LEX converts regular expressions into finite state machines for efficient pattern matching.

#### Example: Recognizing Integer
```
Pattern: [0-9]+

State Machine:
Start → (digit) → Accept State
       ↑         ↓
       └─(digit)─┘
```

---

## LEX Syntax and Structure

### Basic LEX Program Structure
```lex
%{
/* C declarations and includes */
#include <stdio.h>
int token_count = 0;
%}

/* LEX definitions section */
DIGIT    [0-9]
LETTER   [a-zA-Z]

%%
/* Rules section */
{DIGIT}+        { printf("INTEGER: %s\n", yytext); token_count++; }
{LETTER}+       { printf("WORD: %s\n", yytext); token_count++; }
[ \t\n]         { /* ignore whitespace */ }
.               { printf("UNKNOWN: %s\n", yytext); }

%%
/* User code section */
int main() {
    yylex();
    printf("Total tokens: %d\n", token_count);
    return 0;
}

int yywrap() {
    return 1;  /* End of input */
}
```

### Three Main Sections:

#### 1. **Declarations Section** `%{ ... %}`
- C code that gets copied to the beginning of generated file
- Include statements, global variables, function prototypes
- Type definitions and constants

#### 2. **Definitions Section**
- Define named patterns for reuse
- Set options and start conditions
- Format: `NAME pattern`

#### 3. **Rules Section** `%% ... %%`
- Pattern-action pairs
- Format: `pattern { action }`
- Actions are C code executed when pattern matches

#### 4. **User Code Section**
- Additional C functions
- Usually contains `main()` and `yywrap()`
- Gets copied to end of generated file

### Built-in Variables and Functions:

#### Variables:
- **`yytext`**: Contains the matched text (lexeme)
- **`yyleng`**: Length of matched text
- **`yylineno`**: Current line number (with `%option yylineno`)
- **`yyin`**: Input file pointer (default: stdin)
- **`yyout`**: Output file pointer (default: stdout)

#### Functions:
- **`yylex()`**: Main lexical analysis function
- **`yywrap()`**: Called at end of input (return 1 to stop, 0 to continue)
- **`input()`**: Read next character from input
- **`unput(c)`**: Put character back into input stream
- **`output(c)`**: Write character to output
- **`ECHO`**: Output the matched text

---

## Regular Expressions in LEX

### Basic Patterns:

#### Character Classes:
```lex
[abc]           # Matches 'a', 'b', or 'c'
[a-z]           # Matches any lowercase letter
[A-Z]           # Matches any uppercase letter
[0-9]           # Matches any digit
[a-zA-Z0-9]     # Matches alphanumeric characters
[^abc]          # Matches anything except 'a', 'b', or 'c'
```

#### Quantifiers:
```lex
a*              # Zero or more 'a's
a+              # One or more 'a's
a?              # Zero or one 'a'
a{3}            # Exactly 3 'a's
a{2,5}          # Between 2 and 5 'a's
a{3,}           # 3 or more 'a's
```

#### Special Characters:
```lex
.               # Any character except newline
^               # Beginning of line
$               # End of line
\n              # Newline
\t              # Tab
\\              # Backslash
\"              # Double quote
```

#### Grouping and Alternation:
```lex
(abc)           # Group 'abc' together
abc|def         # Matches 'abc' or 'def'
(a|b)c          # Matches 'ac' or 'bc'
```

### Common Programming Language Patterns:

#### Identifiers:
```lex
[a-zA-Z_][a-zA-Z0-9_]*
```

#### Integers:
```lex
[0-9]+
-?[0-9]+                    # With optional minus sign
0[xX][0-9a-fA-F]+          # Hexadecimal
0[0-7]+                     # Octal
```

#### Floating Point Numbers:
```lex
[0-9]+\.[0-9]+                           # Basic float: 123.45
[0-9]*\.[0-9]+([eE][+-]?[0-9]+)?        # Scientific notation
[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?        # Optional fractional part
```

#### String Literals:
```lex
\"([^"\n]|(\\.))*\"         # Double-quoted strings with escapes
'([^'\n]|(\\.))*'           # Single-quoted strings
```

#### Comments:
```lex
\/\/.*                      # Single-line comments: //
\/\*([^*]|\*[^/])*\*\/     # Multi-line comments: /* */
```

### Advanced Pattern Techniques:

#### Lookahead and Context:
```lex
abc/def         # Match 'abc' only if followed by 'def'
^abc            # Match 'abc' only at beginning of line
abc$            # Match 'abc' only at end of line
```

#### Named Patterns:
```lex
DIGIT    [0-9]
LETTER   [a-zA-Z]
ID       {LETTER}({LETTER}|{DIGIT})*

%%
{ID}            { printf("Identifier: %s\n", yytext); }
{DIGIT}+        { printf("Number: %s\n", yytext); }
```

---

## Advanced LEX Features

### Start Conditions (States)
LEX supports different scanning contexts using start conditions.

#### Exclusive States:
```lex
%x COMMENT STRING

%%
"/*"                { BEGIN(COMMENT); }
<COMMENT>"*/"       { BEGIN(INITIAL); }
<COMMENT>\n         { /* count lines in comments */ }
<COMMENT>.          { /* ignore comment content */ }

"\""                { BEGIN(STRING); }
<STRING>"\""        { BEGIN(INITIAL); }
<STRING>\n          { printf("ERROR: Unterminated string\n"); }
<STRING>.           { /* process string content */ }
```

#### Inclusive States:
```lex
%s SPECIAL

%%
<INITIAL,SPECIAL>normal_pattern    { /* action */ }
<SPECIAL>special_pattern           { /* special action */ }
```

### Options and Directives:

#### Common Options:
```lex
%option yylineno        # Enable line counting
%option noyywrap        # Don't require yywrap() function
%option case-insensitive # Ignore case in patterns
%option debug           # Enable debug output
%option stack           # Enable start condition stack
```

#### Example with Options:
```lex
%option yylineno noyywrap

%%
[0-9]+          { printf("Line %d: Number %s\n", yylineno, yytext); }
[a-zA-Z]+       { printf("Line %d: Word %s\n", yylineno, yytext); }
\n              { /* newlines handled automatically */ }
.               { /* ignore other characters */ }
```

### Multiple Input Files:
```lex
%{
int current_file = 0;
char *filenames[] = {"file1.txt", "file2.txt", NULL};
%}

%%
<<EOF>>         {
                    if (filenames[++current_file] != NULL) {
                        yyin = fopen(filenames[current_file], "r");
                        return; /* continue scanning */
                    } else {
                        yyterminate(); /* end scanning */
                    }
                }
```

### Token Return Values:
```lex
%{
enum {
    TOKEN_NUMBER = 258,
    TOKEN_IDENTIFIER = 259,
    TOKEN_PLUS = 260
};
%}

%%
[0-9]+          { return TOKEN_NUMBER; }
[a-zA-Z]+       { return TOKEN_IDENTIFIER; }
"+"             { return TOKEN_PLUS; }
[ \t\n]         { /* ignore whitespace */ }
```

---

## Integration with C Programming

### Interfacing with Parser (YACC/Bison):

#### LEX File (`scanner.l`):
```lex
%{
#include "parser.tab.h"  /* Generated by YACC */
%}

%%
[0-9]+          { yylval.ival = atoi(yytext); return NUMBER; }
[a-zA-Z]+       { yylval.sval = strdup(yytext); return IDENTIFIER; }
"+"             { return PLUS; }
"*"             { return MULTIPLY; }
"("             { return LPAREN; }
")"             { return RPAREN; }
[ \t\n]         { /* ignore whitespace */ }
.               { return yytext[0]; }
```

#### YACC File (`parser.y`):
```yacc
%{
#include <stdio.h>
int yylex();
void yyerror(char *);
%}

%union {
    int ival;
    char *sval;
}

%token <ival> NUMBER
%token <sval> IDENTIFIER
%token PLUS MULTIPLY LPAREN RPAREN

%%
expression: expression PLUS term    { printf("Addition\n"); }
          | term                    { printf("Term\n"); }
          ;
```

### Data Structures and Symbol Tables:

#### Symbol Table Implementation:
```lex
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct symbol {
    char *name;
    int type;
    int value;
    struct symbol *next;
};

struct symbol *symbol_table = NULL;

struct symbol *lookup(char *name) {
    struct symbol *sp;
    for (sp = symbol_table; sp != NULL; sp = sp->next) {
        if (strcmp(sp->name, name) == 0) {
            return sp;
        }
    }
    return NULL;
}

void insert(char *name, int type) {
    struct symbol *sp = malloc(sizeof(struct symbol));
    sp->name = strdup(name);
    sp->type = type;
    sp->value = 0;
    sp->next = symbol_table;
    symbol_table = sp;
}
%}

%%
[a-zA-Z_][a-zA-Z0-9_]*  {
                            struct symbol *sp = lookup(yytext);
                            if (sp == NULL) {
                                printf("New identifier: %s\n", yytext);
                                insert(yytext, 1);
                            } else {
                                printf("Known identifier: %s\n", yytext);
                            }
                        }
```

### Error Handling:

#### Comprehensive Error Reporting:
```lex
%{
int line_number = 1;
int error_count = 0;

void lex_error(char *message) {
    fprintf(stderr, "Lexical error at line %d: %s\n", line_number, message);
    error_count++;
}
%}

%%
[0-9]+[a-zA-Z]+     { lex_error("Invalid identifier starting with digit"); }
\"[^"]*$           { lex_error("Unterminated string literal"); }
'[^']*$            { lex_error("Unterminated character literal"); }
\n                 { line_number++; }
.                  { lex_error("Unexpected character"); }

%%
int main() {
    yylex();
    if (error_count > 0) {
        printf("Compilation failed with %d errors\n", error_count);
        return 1;
    }
    printf("Lexical analysis completed successfully\n");
    return 0;
}
```

---

## Common Patterns and Examples

### Programming Language Lexical Analyzer:

#### Complete C Language Scanner:
```lex
%option yylineno

%{
#include <stdio.h>
#include <string.h>

/* Token types */
enum token_type {
    KEYWORD, IDENTIFIER, INTEGER, FLOAT, STRING, CHARACTER,
    OPERATOR, PUNCTUATOR, COMMENT, WHITESPACE, ERROR
};

struct {
    enum token_type type;
    int count;
} token_stats[] = {
    {KEYWORD, 0}, {IDENTIFIER, 0}, {INTEGER, 0}, {FLOAT, 0},
    {STRING, 0}, {CHARACTER, 0}, {OPERATOR, 0}, {PUNCTUATOR, 0},
    {COMMENT, 0}, {ERROR, 0}
};

void count_token(enum token_type type) {
    for (int i = 0; i < sizeof(token_stats)/sizeof(token_stats[0]); i++) {
        if (token_stats[i].type == type) {
            token_stats[i].count++;
            break;
        }
    }
}

int is_keyword(char *str) {
    char *keywords[] = {
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "goto", "if",
        "int", "long", "register", "return", "short", "signed", "sizeof",
        "static", "struct", "switch", "typedef", "union", "unsigned", "void",
        "volatile", "while"
    };
    int num_keywords = sizeof(keywords) / sizeof(keywords[0]);
    
    for (int i = 0; i < num_keywords; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}
%}

/* Start conditions for comments */
%x COMMENT

/* Pattern definitions */
DIGIT       [0-9]
LETTER      [a-zA-Z_]
IDENTIFIER  {LETTER}({LETTER}|{DIGIT})*
INTEGER     {DIGIT}+
FLOAT       {DIGIT}+\.{DIGIT}+([eE][+-]?{DIGIT}+)?
OPERATOR    "=="|"!="|"<="|">="|"&&"|"||"|"++"|"--"|"<<"|">>"|[+\-*/%=<>!&|^~]
PUNCTUATOR  [{}()\[\];,.]

%%

{IDENTIFIER}    {
                    if (is_keyword(yytext)) {
                        printf("%-12s %-20s %d\n", "KEYWORD", yytext, yylineno);
                        count_token(KEYWORD);
                    } else {
                        printf("%-12s %-20s %d\n", "IDENTIFIER", yytext, yylineno);
                        count_token(IDENTIFIER);
                    }
                }

{INTEGER}       {
                    printf("%-12s %-20s %d\n", "INTEGER", yytext, yylineno);
                    count_token(INTEGER);
                }

{FLOAT}         {
                    printf("%-12s %-20s %d\n", "FLOAT", yytext, yylineno);
                    count_token(FLOAT);
                }

\"([^"\n]|(\\.))*\" {
                    printf("%-12s %-20s %d\n", "STRING", yytext, yylineno);
                    count_token(STRING);
                }

'([^'\n]|(\\.))'    {
                    printf("%-12s %-20s %d\n", "CHARACTER", yytext, yylineno);
                    count_token(CHARACTER);
                }

{OPERATOR}      {
                    printf("%-12s %-20s %d\n", "OPERATOR", yytext, yylineno);
                    count_token(OPERATOR);
                }

{PUNCTUATOR}    {
                    printf("%-12s %-20s %d\n", "PUNCTUATOR", yytext, yylineno);
                    count_token(PUNCTUATOR);
                }

"/*"            { BEGIN(COMMENT); count_token(COMMENT); }
<COMMENT>"*/"   { BEGIN(INITIAL); }
<COMMENT>\n     { /* handle newlines in comments */ }
<COMMENT>.      { /* ignore comment content */ }

"//".*          { count_token(COMMENT); }

[ \t\r]+        { /* ignore whitespace */ }
\n              { /* newlines handled by yylineno */ }

.               {
                    printf("%-12s %-20s %d\n", "ERROR", yytext, yylineno);
                    count_token(ERROR);
                }

%%

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }
    
    printf("%-12s %-20s %s\n", "TOKEN TYPE", "LEXEME", "LINE");
    printf("%-12s %-20s %s\n", "----------", "------", "----");
    
    yylex();
    
    printf("\n\nToken Statistics:\n");
    printf("================\n");
    char *type_names[] = {
        "Keywords", "Identifiers", "Integers", "Floats",
        "Strings", "Characters", "Operators", "Punctuators",
        "Comments", "Errors"
    };
    
    for (int i = 0; i < sizeof(token_stats)/sizeof(token_stats[0]); i++) {
        printf("%-15s: %d\n", type_names[i], token_stats[i].count);
    }
    
    if (yyin != stdin) fclose(yyin);
    return 0;
}

int yywrap() {
    return 1;
}
```

### Configuration File Parser:

#### INI File Lexical Analyzer:
```lex
%{
#include <stdio.h>
#include <string.h>

typedef enum {
    SECTION_HEADER,
    KEY,
    VALUE,
    COMMENT_LINE,
    ERROR_TOKEN
} token_type_t;

void print_token(token_type_t type, char *text) {
    char *type_names[] = {"SECTION", "KEY", "VALUE", "COMMENT", "ERROR"};
    printf("[%s] %s\n", type_names[type], text);
}
%}

%x VALUE_MODE

%%

^[ \t]*"["[^\]]+"]"[ \t]*$  {
                                /* Remove brackets and whitespace */
                                char *start = strchr(yytext, '[') + 1;
                                char *end = strchr(start, ']');
                                *end = '\0';
                                print_token(SECTION_HEADER, start);
                            }

^[ \t]*[a-zA-Z_][a-zA-Z0-9_]*[ \t]*"=" {
                                /* Extract key name */
                                char key[256];
                                sscanf(yytext, " %[a-zA-Z0-9_] =", key);
                                print_token(KEY, key);
                                BEGIN(VALUE_MODE);
                            }

<VALUE_MODE>[^\n\r]+        {
                                /* Trim leading/trailing whitespace from value */
                                char *start = yytext;
                                while (*start == ' ' || *start == '\t') start++;
                                char *end = start + strlen(start) - 1;
                                while (end > start && (*end == ' ' || *end == '\t')) end--;
                                *(end + 1) = '\0';
                                print_token(VALUE, start);
                                BEGIN(INITIAL);
                            }

^[ \t]*"#".*                { print_token(COMMENT_LINE, yytext); }
^[ \t]*";".*                { print_token(COMMENT_LINE, yytext); }

[ \t\n\r]+                  { /* ignore whitespace */ }

.                           { print_token(ERROR_TOKEN, yytext); }

%%

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }
    
    printf("Parsing INI file...\n");
    yylex();
    
    if (yyin != stdin) fclose(yyin);
    return 0;
}

int yywrap() { return 1; }
```

### Log File Analyzer:

#### Web Server Log Parser:
```lex
%{
#include <stdio.h>
#include <time.h>

struct log_stats {
    int total_requests;
    int get_requests;
    int post_requests;
    int error_4xx;
    int error_5xx;
    long total_bytes;
} stats = {0};

void parse_log_entry(char *line) {
    char ip[16], method[10], url[256], protocol[16];
    int status_code, bytes;
    
    /* Simple parsing - real implementation would be more robust */
    if (sscanf(line, "%s - - [%*[^]]] \"%s %s %s\" %d %d",
               ip, method, url, protocol, &status_code, &bytes) == 6) {
        
        stats.total_requests++;
        stats.total_bytes += bytes;
        
        if (strcmp(method, "GET") == 0) stats.get_requests++;
        else if (strcmp(method, "POST") == 0) stats.post_requests++;
        
        if (status_code >= 400 && status_code < 500) stats.error_4xx++;
        else if (status_code >= 500) stats.error_5xx++;
        
        printf("IP: %-15s Method: %-6s Status: %d Bytes: %d\n",
               ip, method, status_code, bytes);
    }
}
%}

%%

^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+.*$  { parse_log_entry(yytext); }
\n                                  { /* ignore empty lines */ }
.                                   { /* ignore invalid lines */ }

%%

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }
    
    printf("Analyzing web server log...\n\n");
    yylex();
    
    printf("\n\nLog Statistics:\n");
    printf("===============\n");
    printf("Total Requests: %d\n", stats.total_requests);
    printf("GET Requests:   %d\n", stats.get_requests);
    printf("POST Requests:  %d\n", stats.post_requests);
    printf("4xx Errors:     %d\n", stats.error_4xx);
    printf("5xx Errors:     %d\n", stats.error_5xx);
    printf("Total Bytes:    %ld\n", stats.total_bytes);
    
    if (yyin != stdin) fclose(yyin);
    return 0;
}

int yywrap() { return 1; }
```

---

## Debugging and Troubleshooting

### Common Issues and Solutions:

#### 1. **Pattern Conflicts**
```lex
/* PROBLEM: Overlapping patterns */
[0-9]+          { printf("Integer\n"); }
[0-9]+\.[0-9]+  { printf("Float\n"); }  /* This won't match! */

/* SOLUTION: Order patterns correctly */
[0-9]+\.[0-9]+  { printf("Float\n"); }   /* More specific first */
[0-9]+          { printf("Integer\n"); }
```

#### 2. **Infinite Loops**
```lex
/* PROBLEM: Pattern that matches empty string */
[a-z]*          { printf("Letters: %s\n", yytext); }  /* Dangerous! */

/* SOLUTION: Ensure patterns consume characters */
[a-z]+          { printf("Letters: %s\n", yytext); }  /* Safe */
```

#### 3. **Character Escaping**
```lex
/* PROBLEM: Special characters not escaped */
.               { printf("Period\n"); }      /* Matches ANY character */

/* SOLUTION: Escape special characters */
"\."            { printf("Period\n"); }      /* Matches literal period */
```

#### 4. **Memory Leaks with Dynamic Allocation**
```lex
%{
char *string_buffer = NULL;
int string_length = 0;
%}

%x STRING_STATE

%%
"\""                {
                        string_buffer = malloc(1000);
                        string_length = 0;
                        BEGIN(STRING_STATE);
                    }

<STRING_STATE>"\""  {
                        string_buffer[string_length] = '\0';
                        printf("String: %s\n", string_buffer);
                        free(string_buffer);  /* Don't forget to free! */
                        BEGIN(INITIAL);
                    }

<STRING_STATE>.     {
                        if (string_length < 999) {
                            string_buffer[string_length++] = yytext[0];
                        }
                    }
```

### Debugging Techniques:

#### 1. **Enable Debug Mode**
```bash
lex -d scanner.l
gcc lex.yy.c -o scanner
./scanner -d < input.txt
```

#### 2. **Add Debug Output**
```lex
%%
[0-9]+          {
                    printf("DEBUG: Matched integer '%s' at line %d\n", 
                           yytext, yylineno);
                    /* Your normal action here */
                }
```

#### 3. **Pattern Testing**
```lex
%{
#define DEBUG_PATTERN(pattern_name) \
    printf("DEBUG: %s matched '%s'\n", pattern_name, yytext)
%}

%%
[0-9]+          { DEBUG_PATTERN("INTEGER"); }
[a-zA-Z]+       { DEBUG_PATTERN("IDENTIFIER"); }
```

#### 4. **Input Tracing**
```lex
%{
void trace_input() {
    printf("Input position: %ld, Line: %d, Text: '%s'\n", 
           ftell(yyin), yylineno, yytext);
}
%}

%%
.               { trace_input(); }
```

---

## Best Practices

### 1. **Code Organization**

#### Separate Concerns:
```lex
%{
/* scanner.l */
#include "tokens.h"
#include "symbol_table.h"
#include "error_handling.h"

/* Keep LEX file focused on pattern matching */
%}

/* Move complex logic to separate C files */
%%
[a-zA-Z_][a-zA-Z0-9_]*  { return process_identifier(yytext); }
[0-9]+                  { return process_integer(yytext); }
```

#### Use Header Files:
```c
/* tokens.h */
#ifndef TOKENS_H
#define TOKENS_H

typedef enum {
    TOKEN_IDENTIFIER = 258,
    TOKEN_INTEGER = 259,
    TOKEN_FLOAT = 260,
    /* ... */
} token_type_t;

extern int process_identifier(char *text);
extern int process_integer(char *text);

#endif
```

### 2. **Performance Optimization**

#### Minimize Backtracking:
```lex
/* GOOD: Specific patterns first */
"while"         { return WHILE; }
"if"            { return IF; }
[a-zA-Z]+       { return IDENTIFIER; }

/* AVOID: Generic patterns first */
[a-zA-Z]+       { return check_keyword(yytext); }  /* Slower */
```

#### Use Character Classes Efficiently:
```lex
/* GOOD: Use predefined classes */
[[:alpha:]]     { /* faster */ }
[[:digit:]]     { /* faster */ }

/* OKAY: Custom classes */
[a-zA-Z]        { /* reasonable */ }
[0-9]           { /* reasonable */ }

/* AVOID: Complex alternations */
(a|b|c|d|e|f)   { /* slower */ }
```

### 3. **Error Handling**

#### Comprehensive Error Reporting:
```lex
%{
typedef struct error_info {
    int line;
    int column;
    char *message;
    char *context;
} error_info_t;

void report_error(char *message) {
    fprintf(stderr, "Lexical error at line %d, column %d: %s\n",
            yylineno, yyleng, message);
    fprintf(stderr, "Context: '%s'\n", yytext);
}
%}

%%
[0-9]+[a-zA-Z]+     { report_error("Invalid identifier starting with digits"); }
\"[^"]*$           { report_error("Unterminated string literal"); }
.                   { report_error("Unexpected character"); }
```

#### Graceful Error Recovery:
```lex
%{
int error_count = 0;
const int MAX_ERRORS = 10;
%}

%%
.   {
        if (++error_count > MAX_ERRORS) {
            fprintf(stderr, "Too many errors, aborting\n");
            exit(1);
        }
        fprintf(stderr, "Skipping invalid character: '%c'\n", yytext[0]);
    }
```

### 4. **Maintainable Code**

#### Use Named Patterns:
```lex
/* GOOD: Readable definitions */
DIGIT           [0-9]
LETTER          [a-zA-Z]
IDENTIFIER      {LETTER}({LETTER}|{DIGIT}|_)*
INTEGER         {DIGIT}+
FLOAT           {DIGIT}+\.{DIGIT}+

%%
{IDENTIFIER}    { /* action */ }
{INTEGER}       { /* action */ }
{FLOAT}         { /* action */ }
```

#### Document Complex Patterns:
```lex
/* Email address pattern - RFC 5322 simplified */
EMAIL_LOCAL     [a-zA-Z0-9._%+-]+
EMAIL_DOMAIN    [a-zA-Z0-9.-]+
EMAIL_TLD       [a-zA-Z]{2,}
EMAIL           {EMAIL_LOCAL}@{EMAIL_DOMAIN}\.{EMAIL_TLD}

/* URL pattern - simplified HTTP/HTTPS */
PROTOCOL        https?
DOMAIN          [a-zA-Z0-9.-]+
PATH            [a-zA-Z0-9./_-]*
URL             {PROTOCOL}:\/\/{DOMAIN}(\/({PATH})?)?

%%
{EMAIL}         { process_email(yytext); }
{URL}           { process_url(yytext); }
```

---

## Real-World Applications

### 1. **Compiler Construction**

#### Multi-Language Compiler Frontend:
```lex
%{
/* Universal source code lexer */
#include "language_detector.h"
#include "token_processor.h"

language_t current_language = LANG_UNKNOWN;
%}

%x C_MODE PYTHON_MODE JAVA_MODE

%%

/* Language detection based on file extensions or headers */
^"#!/usr/bin/python"    { current_language = LANG_PYTHON; BEGIN(PYTHON_MODE); }
^"#include"             { current_language = LANG_C; BEGIN(C_MODE); }
^"package"[ \t]+        { current_language = LANG_JAVA; BEGIN(JAVA_MODE); }

<C_MODE>{
    "int"|"char"|"float"        { return process_c_keyword(yytext); }
    [a-zA-Z_][a-zA-Z0-9_]*      { return process_c_identifier(yytext); }
    "//".*                      { return process_c_comment(yytext); }
}

<PYTHON_MODE>{
    "def"|"class"|"import"      { return process_python_keyword(yytext); }
    [a-zA-Z_][a-zA-Z0-9_]*      { return process_python_identifier(yytext); }
    "#".*                       { return process_python_comment(yytext); }
}

<JAVA_MODE>{
    "public"|"class"|"static"   { return process_java_keyword(yytext); }
    [a-zA-Z_][a-zA-Z0-9_]*      { return process_java_identifier(yytext); }
    "//".*                      { return process_java_comment(yytext); }
}
```

### 2. **Data Processing Pipelines**

#### Log Analysis System:
```lex
%{
#include "log_analyzer.h"
#include "database.h"
#include "statistics.h"

typedef struct log_entry {
    char timestamp[32];
    char level[16];
    char component[64];
    char message[512];
} log_entry_t;

log_entry_t current_entry;
%}

TIMESTAMP   [0-9]{4}-[0-9]{2}-[0-9]{2}[ ][0-9]{2}:[0-9]{2}:[0-9]{2}
LEVEL       (DEBUG|INFO|WARN|ERROR|FATAL)
COMPONENT   [A-Za-z][A-Za-z0-9._-]*

%%

{TIMESTAMP}     { strncpy(current_entry.timestamp, yytext, 31); }
{LEVEL}         { 
                    strncpy(current_entry.level, yytext, 15);
                    update_level_stats(yytext);
                }
{COMPONENT}     { strncpy(current_entry.component, yytext, 63); }
.*              { 
                    strncpy(current_entry.message, yytext, 511);
                    store_log_entry(&current_entry);
                    analyze_patterns(&current_entry);
                }
\n              { memset(&current_entry, 0, sizeof(current_entry)); }
```

### 3. **Configuration Management**

#### Multi-Format Configuration Parser:
```lex
%{
#include "config_manager.h"

typedef enum {
    CONFIG_INI,
    CONFIG_JSON,
    CONFIG_YAML,
    CONFIG_XML
} config_format_t;

config_format_t format = CONFIG_INI;
%}

%x JSON_MODE YAML_MODE XML_MODE

%%

/* Auto-detect format */
^[ \t]*"{"              { format = CONFIG_JSON; BEGIN(JSON_MODE); }
^[a-zA-Z_][^:]*":"      { format = CONFIG_YAML; BEGIN(YAML_MODE); }
^[ \t]*"<"[^>]*">"      { format = CONFIG_XML; BEGIN(XML_MODE); }

<JSON_MODE>{
    "\""[^"]*"\""[ \t]*":"[ \t]*"\""[^"]*"\""    {
        parse_json_string_pair(yytext);
    }
    "\""[^"]*"\""[ \t]*":"[ \t]*[0-9]+          {
        parse_json_number_pair(yytext);
    }
}

<YAML_MODE>{
    ^[a-zA-Z_][^:]*":"[ \t]*.*$     {
        parse_yaml_key_value(yytext);
    }
    ^[ \t]+"- ".*$                  {
        parse_yaml_list_item(yytext);
    }
}

<XML_MODE>{
    "<"[^>]+">"[^<]*"</"[^>]+">"    {
        parse_xml_element(yytext);
    }
}

/* Default INI format */
^[a-zA-Z_][^=]*"=".*$   { parse_ini_assignment(yytext); }
^"["[^\]]+"]"           { parse_ini_section(yytext); }
```

### 4. **Scientific Data Processing**

#### Bioinformatics Sequence Analyzer:
```lex
%{
#include "sequence_analysis.h"

typedef struct {
    int a_count, t_count, g_count, c_count;
    int gc_content;
    int length;
} dna_stats_t;

dna_stats_t stats = {0};
%}

%x FASTA_SEQUENCE

%%

^">".*          {
                    /* FASTA header */
                    if (stats.length > 0) {
                        finalize_sequence_analysis(&stats);
                    }
                    initialize_new_sequence(yytext);
                    BEGIN(FASTA_SEQUENCE);
                }

<FASTA_SEQUENCE>[ATGC]+  {
                    for (int i = 0; i < yyleng; i++) {
                        switch (yytext[i]) {
                            case 'A': stats.a_count++; break;
                            case 'T': stats.t_count++; break;
                            case 'G': stats.g_count++; break;
                            case 'C': stats.c_count++; break;
                        }
                    }
                    stats.length += yyleng;
                }

<FASTA_SEQUENCE>\n      { /* ignore newlines in sequence */ }

<FASTA_SEQUENCE>[^ATGC\n]+ {
                    report_invalid_nucleotides(yytext);
                }
```

### 5. **Network Protocol Analysis**

#### HTTP Request Parser:
```lex
%{
#include "http_analyzer.h"

typedef struct http_request {
    char method[16];
    char url[512];
    char version[16];
    char headers[1024];
    char body[2048];
} http_request_t;

http_request_t request;
%}

%x HEADERS BODY

METHOD      (GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)
URL         [^ \t\n]+
VERSION     HTTP\/[0-9]+\.[0-9]+

%%

{METHOD}        { strncpy(request.method, yytext, 15); }
{URL}           { strncpy(request.url, yytext, 511); }
{VERSION}       { 
                    strncpy(request.version, yytext, 15); 
                    BEGIN(HEADERS);
                }

<HEADERS>^[A-Za-z-]+":".*$  {
                    strncat(request.headers, yytext, 
                           sizeof(request.headers) - strlen(request.headers) - 1);
                }

<HEADERS>^\r?\n$    { BEGIN(BODY); }

<BODY>.*            {
                    strncpy(request.body, yytext, 2047);
                    process_http_request(&request);
                    memset(&request, 0, sizeof(request));
                    BEGIN(INITIAL);
                }
```

---

## Advanced Topics and Future Directions

### Integration with Modern Tools

#### 1. **LEX with Modern Build Systems**
```makefile
# Makefile integration
%.c: %.l
	flex -o $@ $<

scanner.o: scanner.c
	gcc -c -o $@ $<

mycompiler: scanner.o parser.o main.o
	gcc -o $@ $^
```

#### 2. **Unicode and Internationalization**
```lex
%option yylineno
%{
#include <locale.h>
#include <wchar.h>

/* Enable Unicode support */
%}

%%

[\u00C0-\u017F]+    { printf("Accented characters: %s\n", yytext); }
[\u4E00-\u9FFF]+    { printf("Chinese characters: %s\n", yytext); }
[\u0400-\u04FF]+    { printf("Cyrillic characters: %s\n", yytext); }
```

#### 3. **Integration with IDEs and Language Servers**
```lex
%{
/* LSP (Language Server Protocol) integration */
#include "lsp_interface.h"

void send_token_info(int line, int column, char *text, int type) {
    lsp_token_t token = {
        .line = line,
        .column = column,
        .length = strlen(text),
        .type = type
    };
    lsp_send_token(&token);
}
%}

%%

[a-zA-Z_][a-zA-Z0-9_]*  {
                            send_token_info(yylineno, yycolumn, yytext, TOKEN_IDENTIFIER);
                        }
```

### Performance Optimization Techniques

#### 1. **Memory Pool Allocation**
```lex
%{
#include "memory_pool.h"

memory_pool_t *token_pool;

void* fast_alloc(size_t size) {
    return pool_alloc(token_pool, size);
}
%}

%%

[a-zA-Z]+       {
                    char *token = fast_alloc(yyleng + 1);
                    strcpy(token, yytext);
                    /* Process token */
                }
```

#### 2. **Parallel Processing**
```lex
%{
#include <pthread.h>
#include "thread_pool.h"

void process_token_async(char *token, int type) {
    token_task_t *task = create_token_task(token, type);
    thread_pool_submit(task);
}
%}

%%

[a-zA-Z]+       { process_token_async(yytext, TOKEN_IDENTIFIER); }
[0-9]+          { process_token_async(yytext, TOKEN_NUMBER); }
```

---

## Conclusion

LEX is a powerful and versatile tool for lexical analysis that forms the foundation of many text processing applications, from simple pattern matching to complex compiler construction. Understanding its capabilities, patterns, and best practices is essential for anyone working in:

- **Compiler Design**: Building lexical analyzers for programming languages
- **Data Processing**: Analyzing log files, configuration files, and structured data
- **Text Analysis**: Processing natural language and extracting information
- **Protocol Analysis**: Parsing network protocols and data formats
- **Scientific Computing**: Processing domain-specific data formats

### Key Takeaways:

1. **Pattern Mastery**: Understanding regular expressions is crucial for effective LEX programming
2. **State Management**: Using start conditions enables complex parsing scenarios
3. **Integration**: LEX works best when integrated with other tools and languages
4. **Performance**: Careful pattern design and optimization techniques improve efficiency
5. **Maintainability**: Well-structured code with clear patterns and documentation is essential

### Next Steps:

- Practice with the provided examples and modify them for your specific needs
- Experiment with different pattern combinations and state management
- Integrate LEX with parser generators like YACC or Bison
- Explore modern alternatives like ANTLR for more complex language processing
- Study real-world lexical analyzers in open-source compilers

LEX remains a fundamental tool in the computer science toolkit, and mastering it provides deep insights into how computers process and understand human-readable text and code.

---

*This guide serves as a comprehensive reference for LEX programming. For the most up-to-date information and advanced features, consult the official LEX/Flex documentation and relevant academic resources.*