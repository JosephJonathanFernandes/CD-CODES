# Compiler Design Laboratory -├── expt3/                            # Experiment 3: Text Analysis
│   ├── README.md
│   ├── expt3a.l                      # Word frequency analyzer
│   ├── input.txt                     # Sample input file
│   ├── lex.exe
│   └── lex.yy.c
├── expt4/                            # Experiment 4: FIRST and FOLLOW Sets
│   ├── README.md
│   ├── expt4a.py                     # FIRST and FOLLOW calculator
│   └── grammar.txt                   # Sample grammar file
└── expt5/                            # Experiment 5: Left-Recursion Elimination
    ├── README.md
    ├── expt5a.py                     # Left-recursion elimination tool
    └── grammar.txt                   # Sample left-recursive grammarrograms

This repository contains a collection of LEX (Lexical Analyzer Generator) programs developed for compiler design laboratory sessions. LEX is a tool for generating lexical analyzers, which are used in the first phase of compilation to break down source code into tokens.

## 📁 Repository Structure

```
compiler design/
├── README.md                          # This file
├── example.l                          # Basic LEX example
├── count_tokens.l                     # Token counting program
├── lex.exe                           # LEX executable
├── lex.yy.c                          # Generated C code
├── LAB SESSION 1 INTRODUCTION TO LEX.docx
├── LAB SESSION 2 LEXICAL ANALYZER.docx
├── LAB SESSION 3 TEXT ANALYSIS USING LEX.docx
├── expt1/                            # Experiment 1: Basic LEX Programs
│   ├── README.md
│   ├── expt1a.l                      # Token identification
│   ├── expt1b.l                      # Decimal to hexadecimal converter
│   ├── expt1c.l                      # Line numbering program
│   ├── expt1d.l                      # Average calculator
│   ├── lex.exe
│   └── lex.yy.c
├── expt2/                            # Experiment 2: Lexical Analyzer
│   ├── README.md
│   ├── expt2a.l                      # C language lexical analyzer
│   ├── ex.c                          # Sample C code for testing
│   ├── lex.exe
│   └── lex.yy.c
└── expt3/                            # Experiment 3: Text Analysis
    ├── README.md
    ├── expt3a.l                      # Word frequency analyzer
    ├── input.txt                     # Sample input file
    ├── lex.exe
    └── lex.yy.c
```

## 🚀 Getting Started

### Prerequisites
- **LEX/Flex**: Lexical analyzer generator (for experiments 1-3)
- **Python 3.x**: Python interpreter (for experiments 4-5)
- **GCC**: GNU Compiler Collection (for compiling LEX-generated C code)
- **Windows Environment**: This setup is configured for Windows with PowerShell

### Basic Usage

#### For LEX Programs (Experiments 1-3):
1. Write your LEX program (`.l` file)
2. Generate C code: `lex filename.l`
3. Compile: `gcc lex.yy.c -o program.exe`
4. Run: `.\program.exe`

#### For Python Programs (Experiments 4-5):
1. Edit the grammar file (`grammar.txt`)
2. Run: `python expt4a.py` or `python expt5a.py`

### Quick Test
```powershell
# Navigate to the root directory
cd "c:\Users\Joseph\Desktop\compiler design"

# Test LEX example
lex example.l
gcc lex.yy.c -o example.exe
echo "123 hello 45.67" | .\example.exe

# Test Python grammar tools
cd expt4
python expt4a.py
```

## 📚 Experiments Overview

### Experiment 1: Introduction to LEX
**Location**: `expt1/`
- **expt1a.l**: Identifies integers, real numbers, and words
- **expt1b.l**: Converts decimal numbers to hexadecimal with step-by-step process
- **expt1c.l**: Adds line numbers to input text
- **expt1d.l**: Calculates average of all numbers in input

### Experiment 2: Lexical Analyzer for C Language
**Location**: `expt2/`
- **expt2a.l**: Complete lexical analyzer for C language
  - Recognizes keywords, identifiers, operators, punctuators
  - Handles phone numbers and email addresses
  - Supports single-line and multi-line comments
  - Provides error detection for unknown symbols

### Experiment 3: Text Analysis using LEX
**Location**: `expt3/`
- **expt3a.l**: Word frequency analysis program
  - Counts occurrences of each word in a text file
  - Case-insensitive analysis
  - Alphabetically sorted output
  - Ignores punctuation and numbers

### Experiment 4: FIRST and FOLLOW Sets using Python
**Location**: `expt4/`
- **expt4a.py**: FIRST and FOLLOW set calculator
  - Computes FIRST sets for context-free grammars
  - Calculates FOLLOW sets for parser construction
  - Handles epsilon productions correctly
  - Essential for LL(1) parser design

### Experiment 5: Elimination of Left-Recursion
**Location**: `expt5/`
- **expt5a.py**: Left-recursion elimination tool
  - Transforms left-recursive grammars
  - Enables top-down parser construction
  - Creates equivalent non-left-recursive grammars
  - Handles direct left-recursion automatically

## 🔧 Utility Programs

### Root Directory Programs
- **`example.l`**: Simple token classifier (numbers, words, unknown)
- **`count_tokens.l`**: Counts different types of tokens in C code

## 📖 Learning Objectives

Through these experiments, you will learn:

### Lexical Analysis (Experiments 1-3):
1. **LEX Syntax**: Understanding patterns, actions, and rules
2. **Token Recognition**: Identifying different types of lexical units
3. **State Management**: Using LEX states for complex parsing
4. **File Processing**: Reading from files and processing text
5. **C Integration**: Combining LEX with C programming
6. **Practical Applications**: Real-world lexical analysis scenarios

### Syntax Analysis (Experiments 4-5):
1. **Grammar Theory**: Understanding context-free grammars
2. **FIRST/FOLLOW Sets**: Essential concepts for parser construction
3. **Left-Recursion**: Problems and solutions in top-down parsing
4. **Parser Design**: Foundations of LL(1) and recursive descent parsers
5. **Algorithm Implementation**: Recursive and iterative approaches
6. **Grammar Transformation**: Maintaining language equivalence

## 💡 Key Concepts Covered

### Lexical Analysis:
- **Regular Expressions**: Pattern matching in LEX
- **Token Classification**: Keywords, identifiers, literals, operators
- **Comment Handling**: Single-line and multi-line comments
- **Error Handling**: Detecting and reporting lexical errors
- **Data Structures**: Using arrays and structures for analysis
- **File I/O**: Reading input from files
- **String Processing**: Manipulating and analyzing text

### Syntax Analysis:
- **Context-Free Grammars**: Formal language specification
- **Derivations**: Left-most and right-most derivations
- **Parse Tree Construction**: Syntax tree generation
- **Grammar Transformations**: Left-recursion elimination
- **Set Computations**: FIRST and FOLLOW set algorithms
- **Parser Types**: Top-down vs. bottom-up approaches

## 🔍 How to Use Each Experiment

1. **Navigate** to the specific experiment directory
2. **Read** the individual README.md for detailed instructions
3. **Compile** the LEX program using the provided commands
4. **Test** with the sample inputs provided
5. **Experiment** with your own input files

## 📝 Notes

- All programs are designed to work on Windows with PowerShell
- LEX generates C code that needs to be compiled with GCC
- Each experiment directory contains its own executable and generated files
- Sample input files are provided for testing

## 🤝 Contributing

Feel free to:
- Add more test cases
- Improve existing programs
- Add new LEX programs
- Enhance documentation

## 📄 License

This project is for educational purposes as part of compiler design coursework.

---

**Happy Learning!** 🎓 Explore the fascinating world of lexical analysis and compiler design through these hands-on experiments.