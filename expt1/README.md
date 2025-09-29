# Experiment 1: Introduction to LEX

This directory contains four basic LEX programs that demonstrate fundamental concepts of lexical analysis.

## 📋 Programs Overview

### 1. expt1a.l - Token Identifier
**Purpose**: Identifies and classifies different types of tokens in input text.

**Features**:
- Recognizes integers (e.g., `123`, `456`)
- Identifies real numbers (e.g., `12.34`, `0.567`)
- Detects words/identifiers (e.g., `hello`, `variable`)
- Ignores other characters

**Example Input/Output**:
```
Input: 123 hello 45.67 world 89
Output:
123 is an INTEGER
hello is a WORD
45.67 is a REAL NUMBER
world is a WORD
89 is an INTEGER
```

### 2. expt1b.l - Decimal to Hexadecimal Converter
**Purpose**: Converts decimal numbers to hexadecimal with step-by-step conversion process.

**Features**:
- Reads decimal numbers from input
- Shows detailed conversion steps
- Displays final hexadecimal result
- Educational tool for understanding number base conversion

**Example Input/Output**:
```
Input: 255
Output:
Decimal: 255
Step 1: 255 / 16 = 15, remainder = 15 ('F')
Step 2: 15 / 16 = 0, remainder = 15 ('F')
Hexadecimal: FF
```

### 3. expt1c.l - Line Number Generator
**Purpose**: Adds line numbers to each line of input text.

**Features**:
- Automatically numbers each line
- Preserves original text formatting
- Useful for code listing and documentation

**Example Input/Output**:
```
Input:
This is line one
This is line two
This is line three

Output:
1: This is line one
2: This is line two
3: This is line three
```

### 4. expt1d.l - Average Calculator
**Purpose**: Calculates the average of all numbers found in the input.

**Features**:
- Extracts all integers from mixed text
- Calculates and displays average
- Handles case when no numbers are present
- Shows result with 2 decimal places

**Example Input/Output**:
```
Input: The numbers are 10, 20, and 30
Output: Average = 20.00

Input: No numbers here!
Output: No numbers entered.
```

## 🚀 How to Run

### General Steps for All Programs:

1. **Navigate to experiment directory**:
```powershell
cd "c:\Users\Joseph\Desktop\compiler design\expt1"
```

2. **Compile and run any program** (replace `X` with a, b, c, or d):
```powershell
lex expt1X.l
gcc lex.yy.c -o expt1X.exe
```

### Specific Usage Examples:

#### expt1a.l - Token Identifier
```powershell
lex expt1a.l
gcc lex.yy.c -o expt1a.exe
echo "123 hello 45.67 world" | .\expt1a.exe
```

#### expt1b.l - Decimal to Hex Converter
```powershell
lex expt1b.l
gcc lex.yy.c -o expt1b.exe
echo "255 16 10" | .\expt1b.exe
```

#### expt1c.l - Line Numbering
```powershell
lex expt1c.l
gcc lex.yy.c -o expt1c.exe
echo -e "First line\nSecond line\nThird line" | .\expt1c.exe
```

#### expt1d.l - Average Calculator
```powershell
lex expt1d.l
gcc lex.yy.c -o expt1d.exe
echo "Numbers: 10, 20, 30, 40" | .\expt1d.exe
```

## 📝 Interactive Testing

You can also run programs interactively:

```powershell
# Compile the program
lex expt1a.l
gcc lex.yy.c -o expt1a.exe

# Run interactively
.\expt1a.exe
# Type your input and press Ctrl+Z (Windows) to end input
```

## 🔍 Key Learning Points

### LEX Fundamentals:
- **Pattern Matching**: Using regular expressions to identify tokens
- **Actions**: C code executed when patterns match
- **yytext**: Built-in variable containing matched text
- **printf**: Displaying results and messages

### Regular Expression Patterns:
- `[0-9]+`: One or more digits (integers)
- `[0-9]+"."[0-9]+`: Decimal numbers with mandatory fractional part
- `[a-zA-Z]+`: Alphabetic characters (words)
- `.*\n`: Entire line including newline
- `.|\n`: Any character or newline (catch-all)

### C Integration:
- Global variables for counting and accumulation
- String-to-integer conversion with `atoi()`
- Mathematical operations and formatting
- Control structures (loops, conditionals)

## 🧪 Experiment Suggestions

Try these modifications to enhance your learning:

1. **Modify expt1a.l**:
   - Add recognition for negative numbers
   - Identify scientific notation (e.g., 1.23e-4)
   - Count occurrences of each token type

2. **Enhance expt1b.l**:
   - Add binary conversion
   - Support octal conversion
   - Handle negative numbers

3. **Improve expt1c.l**:
   - Add character and word count per line
   - Skip empty lines from numbering
   - Add timestamps to lines

4. **Extend expt1d.l**:
   - Calculate median and standard deviation
   - Support floating-point numbers
   - Show minimum and maximum values

## 🐛 Common Issues and Solutions

### Compilation Errors:
- **Error**: `lex: command not found`
  - **Solution**: Install Flex (Windows LEX implementation)
- **Error**: `gcc: command not found`
  - **Solution**: Install MinGW or MSYS2

### Runtime Issues:
- **Problem**: Program doesn't respond
  - **Solution**: Input is buffered; press Ctrl+Z to signal end of input
- **Problem**: Unexpected output
  - **Solution**: Check regular expression patterns for overlaps

### Pattern Matching:
- Remember that LEX chooses the **longest match**
- Order of rules matters when patterns overlap
- Use `.|\n` as a catch-all for unmatched characters

## 📚 Related Concepts

- **Finite Automata**: LEX converts patterns to state machines
- **Compiler Phases**: Lexical analysis is the first phase
- **Token Classification**: Foundation for syntax analysis
- **Regular Languages**: Theoretical basis for pattern matching

---

These programs provide a solid foundation for understanding lexical analysis. Experiment with different inputs and modifications to deepen your understanding!