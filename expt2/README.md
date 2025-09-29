# Experiment 2: Lexical Analyzer for C Language

This directory contains a comprehensive lexical analyzer for the C programming language, demonstrating advanced LEX features and real-world compiler design concepts.

## 📋 Program Overview

### expt2a.l - Complete C Language Lexical Analyzer
**Purpose**: A fully functional lexical analyzer that can tokenize C source code into its constituent elements.

**Features**:
- **Keyword Recognition**: Identifies all C keywords (`int`, `float`, `if`, `while`, etc.)
- **Identifier Detection**: Recognizes variable and function names
- **Literal Handling**: Processes integers, floats, strings, and character literals
- **Operator Classification**: Identifies arithmetic, relational, and assignment operators
- **Punctuator Recognition**: Handles braces, parentheses, semicolons, commas
- **Comment Processing**: Supports both single-line (`//`) and multi-line (`/* */`) comments
- **Special Patterns**: Recognizes phone numbers and email addresses
- **Error Detection**: Reports unknown symbols with line numbers
- **Line Tracking**: Maintains accurate line number information

## 🎯 Token Categories

### 1. Keywords
```c
auto, break, case, char, const, continue, default, do, double, 
else, enum, extern, float, for, goto, if, int, long, register, 
return, short, signed, sizeof, static, struct, switch, typedef, 
union, unsigned, void, volatile, while, phone, email
```

### 2. Identifiers
- Variable names: `x`, `count`, `student_name`
- Function names: `main`, `calculateSum`, `printResults`
- Must start with letter or underscore, followed by letters, digits, or underscores

### 3. Literals
- **Integers**: `123`, `0`, `-456`
- **Floats**: `12.34`, `0.5`, `3.14159`
- **Strings**: `"Hello World"`, `"File not found"`
- **Characters**: `'A'`, `'x'`, `'\n'`

### 4. Operators
```c
==  !=  <=  >=  =  +  -  *  /  >  <
```

### 5. Punctuators
```c
{  }  (  )  ;  ,
```

### 6. Special Patterns
- **Phone Numbers**: `9876543210`, `+91-9876543210`
- **Email Addresses**: `user@example.com`, `test.email@domain.org`

### 7. Comments
- **Single-line**: `// This is a comment`
- **Multi-line**: `/* This is a multi-line comment */`

## 🚀 How to Use

### Basic Compilation and Execution:
```powershell
# Navigate to experiment directory
cd "c:\Users\Joseph\Desktop\compiler design\expt2"

# Compile the lexical analyzer
lex expt2a.l
gcc lex.yy.c -o lexer.exe
```

### Test with Sample C Code:
```powershell
# Use the provided sample file
.\lexer.exe < ex.c

# Or pipe C code directly
echo 'int x = 10; float y = 20.5;' | .\lexer.exe
```

### Create Your Own Test File:
```powershell
# Create a test C program
echo 'int main() { return 0; }' > test.c

# Analyze it
.\lexer.exe < test.c
```

## 📊 Sample Input and Output

### Input (ex.c):
```c
int x = 10;
float y = 20.5;
char ch = 'A';
phone p = +91-9876543210;
email e = user@example.com;

if (x < y) {
    x = x + 1;
}
return 0;
```

### Expected Output:
```
<KEYWORD, int>
<IDENTIFIER, x >
<OPERATOR, =>
<INTEGER, 10 >
<PUNCTUATOR, ;>
<KEYWORD, float>
<IDENTIFIER, y >
<OPERATOR, =>
<FLOAT, 20.5 >
<PUNCTUATOR, ;>
<KEYWORD, char>
<IDENTIFIER, ch >
<OPERATOR, =>
<CHAR, 'A'>
<PUNCTUATOR, ;>
<KEYWORD, phone>
<IDENTIFIER, p >
<OPERATOR, =>
<PHONE, +91-9876543210 >
<PUNCTUATOR, ;>
<KEYWORD, email>
<IDENTIFIER, e >
<OPERATOR, =>
<EMAIL, user@example.com >
<PUNCTUATOR, ;>
<KEYWORD, if>
<PUNCTUATOR, (>
<IDENTIFIER, x >
<OPERATOR, <>
<IDENTIFIER, y >
<PUNCTUATOR, )>
<PUNCTUATOR, {>
<IDENTIFIER, x >
<OPERATOR, =>
<IDENTIFIER, x >
<OPERATOR, +>
<INTEGER, 1 >
<PUNCTUATOR, ;>
<PUNCTUATOR, }>
<KEYWORD, return>
<INTEGER, 0 >
<PUNCTUATOR, ;>
```

## 🔧 Advanced Features

### 1. State Management
The analyzer uses LEX exclusive states to handle multi-line comments:
```lex
%x COMMENT
"/*"                      { BEGIN(COMMENT); }
<COMMENT>"*/"             { BEGIN(INITIAL); }
<COMMENT>\n               { lineno++; }
<COMMENT>.                { /* Ignore inside comment */ }
```

### 2. Pattern Matching Techniques
- **String Literals**: `\"([^"\n]|(\\.))*\"` - Handles escape sequences
- **Character Literals**: `\'([^'\n]|(\\.))\'` - Supports escaped characters
- **Phone Numbers**: `(\+91-)?[0-9]{10}` - Optional country code
- **Email**: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` - Standard email format

### 3. Error Handling
```lex
.  { printf("ERROR: Unknown symbol '%s' at line %d\n", yytext, lineno); }
```

## 🧪 Testing Scenarios

### 1. Basic C Program
```c
#include <stdio.h>
int main() {
    printf("Hello World");
    return 0;
}
```

### 2. Complex Expressions
```c
int result = (a + b) * (c - d) / e;
if (result >= threshold && flag != 0) {
    processResult(result);
}
```

### 3. Comments and Strings
```c
/* Multi-line comment
   spanning several lines */
char message[] = "Hello \"World\""; // Single-line comment
```

### 4. Special Data Types
```c
phone mobile = +91-9876543210;
email contact = john.doe@company.com;
```

## 🎓 Learning Objectives

### LEX Concepts:
- **Exclusive States**: Managing different parsing contexts
- **Complex Patterns**: Handling strings, comments, and special formats
- **Token Classification**: Systematic categorization of language elements
- **Error Reporting**: Providing meaningful error messages

### Compiler Design:
- **Lexical Analysis Phase**: First stage of compilation
- **Token Stream Generation**: Output for syntax analysis
- **Symbol Recognition**: Foundation for semantic analysis
- **Language Specification**: Formal definition of language syntax

### Regular Expressions:
- **Character Classes**: `[a-zA-Z]`, `[0-9]`
- **Quantifiers**: `+`, `*`, `?`
- **Grouping**: `(pattern)`
- **Alternation**: `|`
- **Escape Sequences**: `\"`, `\'`

## 🔍 Enhancements and Experiments

### 1. Add More C Features:
```lex
# Preprocessor directives
^#[a-zA-Z]+.*    { printf("<PREPROCESSOR, %s>\n", yytext); }

# Hexadecimal numbers
0[xX][0-9a-fA-F]+  { printf("<HEX_INTEGER, %s>\n", yytext); }

# Floating point with exponent
[0-9]+\.[0-9]+[eE][+-]?[0-9]+  { printf("<SCIENTIFIC, %s>\n", yytext); }
```

### 2. Enhanced Error Reporting:
```lex
[0-9]+[a-zA-Z]+  { printf("ERROR: Invalid identifier '%s' at line %d\n", yytext, lineno); }
```

### 3. Token Statistics:
Add counters for different token types and display summary at the end.

## 🐛 Common Issues and Solutions

### Pattern Conflicts:
- **Problem**: Identifiers matching keywords
- **Solution**: Keywords are matched first due to longer match rule

### String Handling:
- **Problem**: Unclosed strings cause issues
- **Solution**: Pattern includes newline check: `[^"\n]`

### Comment Nesting:
- **Problem**: C doesn't support nested comments
- **Solution**: Current implementation correctly handles this

### Line Counting:
- **Problem**: Line numbers in comments and strings
- **Solution**: Increment `lineno` only for actual newlines

## 📚 Real-World Applications

This lexical analyzer demonstrates concepts used in:
- **C Compilers**: GCC, Clang preprocessing stage
- **IDEs**: Syntax highlighting and error detection
- **Code Analysis Tools**: Static analysis and formatting
- **Language Servers**: IntelliSense and code completion

## 🔗 Integration with Parser

The token stream generated by this lexical analyzer can be fed into:
1. **Syntax Analyzer (Parser)**: Validates grammatical structure
2. **Semantic Analyzer**: Checks type consistency and scope
3. **Code Generator**: Produces target code

---

This experiment provides hands-on experience with real-world lexical analysis, preparing you for advanced compiler design concepts and practical implementation challenges.