# Experiment 5: Elimination of Left-Recursion in Context-Free Grammar

This directory contains a Python implementation for eliminating left-recursion from context-free grammars, which is essential for constructing top-down parsers like LL(1) parsers.

## 📋 Program Overview

### expt5a.py - Left-Recursion Elimination Tool
**Purpose**: Transforms left-recursive grammar productions into equivalent non-left-recursive forms to enable top-down parsing.

**Features**:
- **Direct Left-Recursion Elimination**: Removes immediate left-recursive productions
- **Grammar Transformation**: Creates new non-terminals to maintain language equivalence
- **File Input/Output**: Reads grammar from files and displays transformed results
- **Epsilon Production Handling**: Properly manages ε (epsilon) productions in transformations
- **Format Preservation**: Maintains readable grammar format in output
- **Automatic Processing**: Handles multiple left-recursive non-terminals

## 🎯 Theoretical Background

### Left-Recursion Problem
A grammar is **left-recursive** if there exists a non-terminal A such that A ⇒* Aα for some string α. This causes infinite loops in top-down parsers.

### Types of Left-Recursion:

#### 1. Direct (Immediate) Left-Recursion:
```
A → Aα | β
```
Where A appears as the first symbol in at least one production.

#### 2. Indirect Left-Recursion:
```
A → Bγ
B → Aδ | other_productions
```
Where A eventually derives to a string starting with A through other non-terminals.

### Elimination Algorithm
**For Direct Left-Recursion:**

Original Grammar:
```
A → Aα₁ | Aα₂ | ... | Aαₘ | β₁ | β₂ | ... | βₙ
```

Transformed Grammar:
```
A → β₁A' | β₂A' | ... | βₙA'
A' → α₁A' | α₂A' | ... | αₘA' | ε
```

Where A' is a new non-terminal.

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
cd "c:\Users\Joseph\Desktop\compiler design\expt5"

# Run the program
python expt5a.py
```

### Using Custom Grammar:
1. **Edit `grammar.txt`** with your left-recursive grammar
2. **Run the program** to see the transformed grammar

## 📊 Sample Transformation

### Input Grammar (grammar.txt):
```
A -> A a | b
```

### Expected Output:
```
Original Grammar:
A -> A a | b

Grammar after Eliminating Left Recursion:
A -> b A'
A' -> a A' | ε
```

### Transformation Explanation:
1. **Identify left-recursive productions**: `A → A a` (direct left-recursion)
2. **Identify non-left-recursive productions**: `A → b`
3. **Create new non-terminal**: `A'`
4. **Transform productions**:
   - `A → b A'` (non-recursive part + new non-terminal)
   - `A' → a A' | ε` (recursive part + epsilon)

## 🧪 Testing Different Grammars

### Test 1: Simple Expression Grammar
```powershell
# Create left-recursive expression grammar
cat > grammar.txt << 'EOF'
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
EOF

python expt5a.py
```

**Expected Result**:
```
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id
```

### Test 2: Multiple Left-Recursive Productions
```powershell
cat > grammar.txt << 'EOF'
A -> A a | A b | c | d
EOF

python expt5a.py
```

**Expected Result**:
```
A -> c A' | d A'
A' -> a A' | b A' | ε
```

### Test 3: Mixed Grammar
```powershell
cat > grammar.txt << 'EOF'
S -> S a | b
T -> c T | d
EOF

python expt5a.py
```

**Expected Result**:
```
S -> b S'
S' -> a S' | ε
T -> c T | d
```

### Test 4: No Left-Recursion
```powershell
cat > grammar.txt << 'EOF'
A -> a A | b
B -> c B | d
EOF

python expt5a.py
```

**Expected Result**: Grammar remains unchanged (no left-recursion detected).

## 🔧 Grammar File Format

### Input Format:
```
NonTerminal -> production1 | production2 | production3
```

### Example Formats:

#### Mathematical Expressions:
```
expr -> expr + term | expr - term | term
term -> term * factor | term / factor | factor
factor -> ( expr ) | number | identifier
```

#### Programming Language Constructs:
```
stmt -> stmt ; stmt | if_stmt | while_stmt | assign_stmt
if_stmt -> if ( condition ) stmt else stmt
assign_stmt -> id = expr
```

#### List Structures:
```
list -> list , element | element
element -> id | number
```

## 🎓 Algorithm Implementation Details

### Core Algorithm:
```python
def eliminate_left_recursion(grammar):
    new_grammar = defaultdict(list)

    for non_terminal in grammar:
        alpha = []  # Left-recursive parts (A → Aα)
        beta = []   # Non-left-recursive parts (A → β)

        # Classify productions
        for production in grammar[non_terminal]:
            if production[0] == non_terminal:
                # A → Aα (left-recursive)
                alpha.append(production[1:])  # Store α part
            else:
                # A → β (non-left-recursive)
                beta.append(production)

        # Apply transformation if left-recursion exists
        if alpha:
            new_nt = non_terminal + "'"  # Create A'
            
            # A → βA' for each β
            for b in beta:
                new_grammar[non_terminal].append(b + [new_nt])
            
            # A' → αA' for each α
            for a in alpha:
                new_grammar[new_nt].append(a + [new_nt])
            
            # A' → ε
            new_grammar[new_nt].append(["ε"])
        else:
            # No left-recursion, keep original productions
            new_grammar[non_terminal].extend(beta)

    return new_grammar
```

### Grammar Parsing:
```python
def read_grammar_from_file(filename):
    grammar = defaultdict(list)
    with open(filename, "r") as f:
        for line in f:
            if "->" in line:
                lhs, rhs = line.strip().split("->")
                lhs = lhs.strip()
                productions = rhs.strip().split("|")
                for prod in productions:
                    # Split production into symbols
                    grammar[lhs].append(prod.strip().split())
    return grammar
```

### Output Formatting:
```python
def print_grammar(grammar):
    for nt in grammar:
        rhs = [" ".join(p) for p in grammar[nt]]
        print(f"{nt} -> {' | '.join(rhs)}")
```

## 🔍 Advanced Features and Extensions

### 1. Indirect Left-Recursion Elimination:
```python
def eliminate_indirect_left_recursion(grammar):
    non_terminals = list(grammar.keys())
    
    for i in range(len(non_terminals)):
        for j in range(i):
            # Replace Ai → Ajγ with Ai → δ1γ | δ2γ | ... where Aj → δ1 | δ2 | ...
            substitute_productions(grammar, non_terminals[i], non_terminals[j])
        
        # Eliminate direct left-recursion for Ai
        grammar = eliminate_direct_left_recursion(grammar, non_terminals[i])
    
    return grammar
```

### 2. Grammar Validation:
```python
def validate_grammar(grammar):
    issues = []
    
    for nt in grammar:
        for production in grammar[nt]:
            # Check for empty productions (should use ε)
            if not production:
                issues.append(f"Empty production for {nt}")
            
            # Check for undefined non-terminals
            for symbol in production:
                if symbol.isupper() and symbol not in grammar and symbol != "ε":
                    issues.append(f"Undefined non-terminal: {symbol}")
    
    return issues
```

### 3. Language Equivalence Verification:
```python
def verify_equivalence(original_grammar, transformed_grammar):
    # Generate sample strings from both grammars
    original_strings = generate_strings(original_grammar, max_length=10)
    transformed_strings = generate_strings(transformed_grammar, max_length=10)
    
    return original_strings == transformed_strings
```

### 4. Step-by-Step Transformation Display:
```python
def detailed_elimination(grammar):
    print("Step-by-step Left-Recursion Elimination:")
    print("=" * 50)
    
    for nt in grammar:
        print(f"\nProcessing non-terminal: {nt}")
        
        left_recursive = []
        non_left_recursive = []
        
        for prod in grammar[nt]:
            if prod[0] == nt:
                left_recursive.append(prod)
                print(f"  Left-recursive: {nt} -> {' '.join(prod)}")
            else:
                non_left_recursive.append(prod)
                print(f"  Non-left-recursive: {nt} -> {' '.join(prod)}")
        
        if left_recursive:
            print(f"  Creating new non-terminal: {nt}'")
            # Show transformation steps...
```

## 🧪 Complex Examples

### Example 1: Arithmetic Expression Grammar
**Input**:
```
E -> E + E | E * E | ( E ) | id
```

**Output**:
```
E -> ( E ) E' | id E'
E' -> + E E' | * E E' | ε
```

### Example 2: Statement List Grammar
**Input**:
```
stmts -> stmts ; stmt | stmt
stmt -> id = expr | if expr then stmt
expr -> id | num
```

**Output**:
```
stmts -> stmt stmts'
stmts' -> ; stmt stmts' | ε
stmt -> id = expr | if expr then stmt
expr -> id | num
```

### Example 3: Nested List Grammar
**Input**:
```
list -> list , list | ( list ) | item
item -> id | num
```

**Output**:
```
list -> ( list ) list' | item list'
list' -> , list list' | ε
item -> id | num
```

## 🎓 Learning Objectives

### Parser Construction Concepts:
- **Top-Down Parsing**: Enabling recursive descent and LL parsing
- **Grammar Transformation**: Maintaining language equivalence
- **Parser Design**: Understanding parser limitations and solutions

### Theoretical Understanding:
- **Formal Language Theory**: Grammar transformations and equivalence
- **Recursion Types**: Direct vs. indirect recursion
- **Language Properties**: How transformations affect generated languages

### Practical Applications:
- **Compiler Design**: Preparing grammars for parser generators
- **Language Implementation**: Building parsers for programming languages
- **Tool Development**: Creating grammar transformation utilities

## 🔧 Integration with Parser Construction

### Use with LL(1) Parsers:
```python
def create_ll1_parser(grammar):
    # First eliminate left-recursion
    transformed_grammar = eliminate_left_recursion(grammar)
    
    # Compute FIRST and FOLLOW sets
    first_sets = compute_first_sets(transformed_grammar)
    follow_sets = compute_follow_sets(transformed_grammar, first_sets)
    
    # Build parse table
    parse_table = build_parse_table(transformed_grammar, first_sets, follow_sets)
    
    return LL1Parser(parse_table)
```

### Integration with Experiment 4:
```python
# Combined workflow
grammar = read_grammar_from_file("grammar.txt")
transformed_grammar = eliminate_left_recursion(grammar)

# Now compute FIRST and FOLLOW for transformed grammar
first_sets = compute_first(transformed_grammar)
follow_sets = compute_follow(transformed_grammar, first_sets)
```

## 🐛 Troubleshooting

### Common Issues:

#### 1. Indirect Left-Recursion:
```
Problem: Program doesn't detect indirect left-recursion
Solution: Current implementation handles only direct left-recursion
Enhancement: Implement indirect left-recursion elimination algorithm
```

#### 2. Grammar Format Errors:
```
Problem: Parsing errors when reading grammar file
Solution: Ensure proper spacing around -> and | symbols
Example: "A -> B | C" not "A->B|C"
```

#### 3. Symbol Recognition:
```
Problem: Multi-character symbols not recognized properly
Solution: Use proper tokenization or quote multi-character symbols
Example: "expr -> IDENTIFIER | NUMBER"
```

#### 4. Epsilon Representation:
```
Problem: Different epsilon symbols cause issues
Solution: Standardize on ε symbol throughout
```

## 📚 Real-World Applications

### Compiler Tools:
- **Parser Generators**: YACC, Bison, ANTLR preprocessing
- **Language Design**: Ensuring grammars are top-down parseable
- **IDE Tools**: Syntax analysis and error recovery

### Academic Research:
- **Grammar Analysis**: Studying grammar properties and transformations
- **Language Theory**: Understanding formal language hierarchies
- **Algorithm Design**: Developing efficient transformation algorithms

### Industry Applications:
- **DSL Development**: Creating domain-specific language parsers
- **Configuration Languages**: Parsing complex configuration formats
- **Protocol Parsers**: Analyzing communication protocol specifications

## 🔗 Next Steps

After eliminating left-recursion:
1. **Compute FIRST and FOLLOW sets** (Experiment 4)
2. **Build LL(1) parse table**
3. **Implement recursive descent parser**
4. **Add error recovery mechanisms**
5. **Create parse tree visualization**

---

This experiment provides crucial foundation for top-down parser construction, demonstrating how theoretical concepts translate into practical compiler implementation techniques.