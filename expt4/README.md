# Experiment 4: FIRST and FOLLOW Sets using Python

This directory contains a Python implementation for computing FIRST and FOLLOW sets for context-free grammars, which are fundamental concepts in compiler design for building parsers.

## 📋 Program Overview

### expt4a.py - FIRST and FOLLOW Set Calculator
**Purpose**: Computes FIRST and FOLLOW sets for a given context-free grammar to aid in parser construction.

**Features**:
- **FIRST Set Computation**: Determines the set of terminals that can appear at the beginning of strings derived from a non-terminal
- **FOLLOW Set Computation**: Determines the set of terminals that can appear immediately after a non-terminal in valid derivations
- **Grammar File Input**: Reads grammar rules from external text files
- **Epsilon Handling**: Properly handles ε (epsilon) productions
- **Recursive Algorithm**: Implements efficient recursive algorithms for set computation
- **Start Symbol Detection**: Automatically identifies the start symbol as the first non-terminal

## 🎯 Theoretical Background

### FIRST Sets
The FIRST set of a non-terminal A, denoted FIRST(A), is the set of all terminals that can appear at the beginning of strings derived from A.

**Rules for FIRST sets**:
1. If A is a terminal, FIRST(A) = {A}
2. If A → ε, then ε ∈ FIRST(A)
3. If A → X₁X₂...Xₙ, then:
   - Add FIRST(X₁) - {ε} to FIRST(A)
   - If ε ∈ FIRST(X₁), add FIRST(X₂) - {ε} to FIRST(A)
   - Continue until a symbol without ε or end of production

### FOLLOW Sets
The FOLLOW set of a non-terminal A, denoted FOLLOW(A), is the set of terminals that can appear immediately after A in valid derivations.

**Rules for FOLLOW sets**:
1. $ ∈ FOLLOW(S) where S is the start symbol
2. If A → αBβ, then FIRST(β) - {ε} ⊆ FOLLOW(B)
3. If A → αB or A → αBβ where ε ∈ FIRST(β), then FOLLOW(A) ⊆ FOLLOW(B)

## 🚀 How to Use

### Prerequisites:
```powershell
# Ensure Python is installed
python --version
# Should show Python 3.x
```

### Basic Execution:
```powershell
# Navigate to experiment directory
cd "c:\Users\Joseph\Desktop\compiler design\expt4"

# Run the program
python expt4a.py
```

### Using Custom Grammar:
1. **Edit `grammar.txt`** with your grammar rules
2. **Run the program** to see FIRST and FOLLOW sets

## 📊 Sample Analysis

### Input Grammar (grammar.txt):
```
E -> T X
X -> + T X | ε
T -> F Y
Y -> * F Y | ε
F -> ( E ) | id
```

### Expected Output:
```
FIRST sets:
FIRST(E) = {'(', 'id'}
FIRST(X) = {'+', 'ε'}
FIRST(T) = {'(', 'id'}
FIRST(Y) = {'*', 'ε'}
FIRST(F) = {'(', 'id'}

FOLLOW sets:
FOLLOW(E) = {'$', ')'}
FOLLOW(X) = {'$', ')'}
FOLLOW(T) = {'+', '$', ')'}
FOLLOW(Y) = {'+', '$', ')'}
FOLLOW(F) = {'*', '+', '$', ')'}
```

### Analysis Explanation:
- **E can start with**: `(` or `id` (from T → F, F → ( E ) | id)
- **X can start with**: `+` or be empty (ε)
- **E can be followed by**: `$` (end) or `)` (in F → ( E ))
- **T can be followed by**: `+` (from X), `$`, or `)` (inherited from E)

## 🔧 Grammar File Format

### Syntax Rules:
```
NonTerminal -> production1 | production2 | production3
AnotherNT -> rule1 | rule2
```

### Example Grammars:

#### 1. Simple Expression Grammar:
```
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

#### 2. If-Else Statement Grammar:
```
S -> if E then S else S | if E then S | other
E -> id
```

#### 3. Arithmetic Expression Grammar:
```
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id | num
```

## 🧪 Testing Different Grammars

### Test 1: Simple Grammar
```powershell
# Create a simple grammar
echo "S -> a S b | ε" > test_grammar.txt

# Modify the filename in expt4a.py temporarily or copy the content to grammar.txt
echo "S -> a S b | ε" > grammar.txt
python expt4a.py
```

### Test 2: Left-Recursive Grammar
```powershell
echo "A -> A a | b" > grammar.txt
python expt4a.py
```

### Test 3: Complex Grammar
```powershell
# Multiple non-terminals with various rules
cat > grammar.txt << 'EOF'
S -> A B
A -> a | ε  
B -> b C
C -> c | ε
EOF
python expt4a.py
```

## 🎓 Learning Objectives

### Parser Construction:
- **LL(1) Parser Design**: FIRST and FOLLOW sets are essential for LL(1) parsing
- **Parse Table Construction**: These sets help build predictive parsing tables
- **Conflict Detection**: Identify grammar ambiguities and conflicts

### Algorithm Understanding:
- **Recursive Algorithms**: Understanding recursive set computation
- **Fixed-Point Algorithms**: Iterative computation until convergence
- **Graph Traversal**: Following production dependencies

### Grammar Analysis:
- **Grammar Properties**: Understanding grammar characteristics
- **Language Recognition**: Determining what strings a grammar can generate
- **Parser Feasibility**: Checking if grammar is suitable for top-down parsing

## 🔍 Algorithm Implementation Details

### FIRST Set Algorithm:
```python
def compute_first(symbol, grammar, first_sets):
    if symbol in first_sets:
        return first_sets[symbol]  # Memoization
    
    first = set()
    if symbol not in grammar:  # Terminal
        first.add(symbol)
    else:
        for production in grammar[symbol]:
            if production == "ε":
                first.add("ε")
            else:
                # Process each symbol in production
                for char in production:
                    first_char = compute_first(char, grammar, first_sets)
                    first |= (first_char - {"ε"})
                    if "ε" not in first_char:
                        break
                else:
                    first.add("ε")  # All symbols can derive ε
    
    first_sets[symbol] = first
    return first
```

### FOLLOW Set Algorithm:
```python
def compute_follow(symbol, grammar, first_sets, follow_sets, start_symbol):
    if symbol == start_symbol:
        follow_sets[symbol].add("$")  # End marker
    
    for lhs in grammar:
        for production in grammar[lhs]:
            for i, char in enumerate(production):
                if char == symbol:
                    if i + 1 < len(production):
                        # Symbol followed by another symbol
                        next_char = production[i+1]
                        next_first = compute_first(next_char, grammar, first_sets)
                        follow_sets[symbol] |= (next_first - {"ε"})
                        if "ε" in next_first:
                            # If next can be empty, add FOLLOW(lhs)
                            follow_sets[symbol] |= compute_follow(lhs, ...)
                    else:
                        # Symbol at end of production
                        if lhs != symbol:
                            follow_sets[symbol] |= compute_follow(lhs, ...)
    
    return follow_sets[symbol]
```

## 🔧 Enhancements and Extensions

### 1. Enhanced Output Formatting:
```python
def print_formatted_sets(first_sets, follow_sets):
    print("=" * 50)
    print("FIRST and FOLLOW Sets Analysis")
    print("=" * 50)
    
    for nt in first_sets:
        first_str = "{" + ", ".join(sorted(first_sets[nt])) + "}"
        follow_str = "{" + ", ".join(sorted(follow_sets[nt])) + "}"
        print(f"FIRST({nt:2}) = {first_str:15} FOLLOW({nt:2}) = {follow_str}")
```

### 2. Parse Table Generation:
```python
def generate_parse_table(grammar, first_sets, follow_sets):
    table = {}
    for nt in grammar:
        table[nt] = {}
        for production in grammar[nt]:
            first_prod = compute_first_of_production(production, first_sets)
            for terminal in first_prod:
                if terminal != "ε":
                    table[nt][terminal] = production
            
            if "ε" in first_prod:
                for terminal in follow_sets[nt]:
                    table[nt][terminal] = production
    return table
```

### 3. Grammar Validation:
```python
def validate_grammar(grammar, first_sets, follow_sets):
    conflicts = []
    for nt in grammar:
        if len(grammar[nt]) > 1:
            # Check for FIRST-FIRST conflicts
            first_intersection = set()
            for prod in grammar[nt]:
                prod_first = compute_first_of_production(prod, first_sets)
                if first_intersection & prod_first:
                    conflicts.append(f"FIRST-FIRST conflict in {nt}")
                first_intersection |= prod_first
    return conflicts
```

## 🐛 Common Issues and Solutions

### Grammar Format Issues:
```
Error: KeyError when processing grammar
Solution: Check grammar.txt format - ensure spaces around ->
```

### Epsilon Representation:
```
Problem: Different epsilon symbols (ε, epsilon, λ)
Solution: Use consistent ε symbol in grammar file
```

### Infinite Recursion:
```
Problem: Stack overflow in recursive calls
Solution: Add memoization and cycle detection
```

### File Encoding:
```
Problem: Unicode characters not recognized
Solution: Save grammar.txt with UTF-8 encoding
```

## 📚 Real-World Applications

### Compiler Construction:
- **Parser Generators**: Tools like YACC, Bison use these concepts
- **Language Design**: Ensuring grammars are parseable
- **IDE Development**: Syntax highlighting and error detection

### Academic Applications:
- **Formal Language Theory**: Understanding language properties
- **Automata Theory**: Relationship with pushdown automata
- **Algorithm Design**: Recursive and dynamic programming techniques

### Industry Tools:
- **Parser Libraries**: ANTLR, JavaCC, and similar tools
- **Domain-Specific Languages**: Creating custom language parsers
- **Configuration Parsers**: Parsing complex configuration formats

## 🔗 Integration with Other Experiments

This experiment builds on:
- **Experiments 1-3**: Lexical analysis provides tokens for parsing
- **Experiment 5**: Left recursion elimination prepares grammars for LL parsing

Next steps:
- Build LL(1) parser using computed sets
- Implement recursive descent parser
- Create parse tree visualization

---

This experiment provides essential foundation for understanding parser construction and grammar analysis, bridging the gap between lexical analysis and syntax analysis in compiler design.