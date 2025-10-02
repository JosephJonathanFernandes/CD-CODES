from collections import defaultdict

# Function to compute FIRST set
def compute_first(symbol, grammar, first_sets, depth=0):
    indent = "  " * depth
    print(f"{indent}Computing FIRST({symbol})")
    
    if symbol in first_sets:
        print(f"{indent}FIRST({symbol}) already computed = {first_sets[symbol]}")
        return first_sets[symbol]
    
    first = set()
    if symbol not in grammar:  # terminal
        first.add(symbol)
        print(f"{indent}{symbol} is terminal, so FIRST({symbol}) = {{{symbol}}}")
    else:
        print(f"{indent}{symbol} is non-terminal with productions: {grammar[symbol]}")
        for i, production in enumerate(grammar[symbol]):
            print(f"{indent}  Production {i+1}: {symbol} -> {' '.join(production)}")
            if production == ["ε"]:  # epsilon
                first.add("ε")
                print(f"{indent}    This is epsilon production, adding ε to FIRST({symbol})")
            else:
                print(f"{indent}    Processing symbols in production...")
                all_have_epsilon = True
                for j, char in enumerate(production):
                    print(f"{indent}    Processing symbol {j+1}: {char}")
                    first_char = compute_first(char, grammar, first_sets, depth+2)
                    first |= (first_char - {"ε"})
                    print(f"{indent}    Adding FIRST({char}) - {{ε}} = {first_char - {'ε'}} to FIRST({symbol})")
                    print(f"{indent}    Current FIRST({symbol}) = {first}")
                    if "ε" not in first_char:
                        print(f"{indent}    {char} doesn't have ε, stopping here for this production")
                        all_have_epsilon = False
                        break
                    else:
                        print(f"{indent}    {char} has ε, continuing to next symbol")
                if all_have_epsilon:
                    first.add("ε")
                    print(f"{indent}    All symbols in production can derive ε, adding ε to FIRST({symbol})")
    
    first_sets[symbol] = first
    print(f"{indent}Final FIRST({symbol}) = {first}")
    return first

# Function to compute FOLLOW set
def compute_follow(symbol, grammar, first_sets, follow_sets, start_symbol, depth=0):
    indent = "  " * depth
    print(f"{indent}Computing FOLLOW({symbol})")
    
    if symbol == start_symbol and "$" not in follow_sets[symbol]:
        follow_sets[symbol].add("$")
        print(f"{indent}{symbol} is start symbol, adding $ to FOLLOW({symbol})")
    
    initial_size = len(follow_sets[symbol])
    
    for lhs in grammar:
        for prod_num, production in enumerate(grammar[lhs]):
            print(f"{indent}  Checking production: {lhs} -> {' '.join(production)}")
            for i, char in enumerate(production):
                if char == symbol:
                    print(f"{indent}    Found {symbol} at position {i}")
                    # Case 1: next symbol exists
                    if i + 1 < len(production):
                        next_char = production[i+1]
                        print(f"{indent}    Next symbol is {next_char}")
                        next_first = compute_first(next_char, grammar, first_sets, depth+1)
                        before_add = follow_sets[symbol].copy()
                        follow_sets[symbol] |= (next_first - {"ε"})
                        added = follow_sets[symbol] - before_add
                        if added:
                            print(f"{indent}    Adding FIRST({next_char}) - {{ε}} = {next_first - {'ε'}} to FOLLOW({symbol})")
                        print(f"{indent}    Current FOLLOW({symbol}) = {follow_sets[symbol]}")
                        
                        if "ε" in next_first:
                            print(f"{indent}    {next_char} can derive ε, need to add FOLLOW({lhs}) to FOLLOW({symbol})")
                            if lhs != symbol:
                                before_recursive = follow_sets[symbol].copy()
                                follow_lhs = compute_follow(lhs, grammar, first_sets, follow_sets, start_symbol, depth+1)
                                follow_sets[symbol] |= (follow_lhs - {"ε"})
                                added_recursive = follow_sets[symbol] - before_recursive
                                if added_recursive:
                                    print(f"{indent}    Added FOLLOW({lhs}) = {added_recursive} to FOLLOW({symbol})")
                            else:
                                print(f"{indent}    {lhs} == {symbol}, skipping to avoid infinite recursion")
                    else:
                        print(f"{indent}    {symbol} is at the end of production")
                        if lhs != symbol:
                            print(f"{indent}    Need to add FOLLOW({lhs}) to FOLLOW({symbol})")
                            before_recursive = follow_sets[symbol].copy()
                            follow_lhs = compute_follow(lhs, grammar, first_sets, follow_sets, start_symbol, depth+1)
                            follow_sets[symbol] |= (follow_lhs - {"ε"})
                            added_recursive = follow_sets[symbol] - before_recursive
                            if added_recursive:
                                print(f"{indent}    Added FOLLOW({lhs}) = {added_recursive} to FOLLOW({symbol})")
                        else:
                            print(f"{indent}    {lhs} == {symbol}, skipping to avoid infinite recursion")
    
    if len(follow_sets[symbol]) > initial_size:
        print(f"{indent}Updated FOLLOW({symbol}) = {follow_sets[symbol]}")
    else:
        print(f"{indent}No new symbols added to FOLLOW({symbol}) = {follow_sets[symbol]}")
    
    return follow_sets[symbol]

# ---------------- MAIN ----------------
def main():
    grammar = defaultdict(list)
    filename = "grammar.txt"

    # Read grammar from file
    with open(filename, "r") as f:
        for line in f:
            if "->" in line:
                lhs, rhs = line.strip().split("->")
                lhs = lhs.strip()
                productions = rhs.strip().split("|")
                for prod in productions:
                    # Replace 'epsilon' with 'ε' automatically
                    prod_symbols = prod.strip().split()
                    prod_symbols = ["ε" if sym.lower() == "epsilon" else sym for sym in prod_symbols]
                    grammar[lhs].append(prod_symbols)

    first_sets = {}
    follow_sets = defaultdict(set)
    start_symbol = list(grammar.keys())[0]  # first non-terminal is start

    # Compute FIRST sets for non-terminals only
    print("=" * 50)
    print("COMPUTING FIRST SETS")
    print("=" * 50)
    for non_terminal in grammar:
        print(f"\n--- Computing FIRST({non_terminal}) ---")
        compute_first(non_terminal, grammar, first_sets)
        print(f"--- FIRST({non_terminal}) = {first_sets[non_terminal]} ---\n")

    # Compute FOLLOW sets for non-terminals only
    print("\n" + "=" * 50)
    print("COMPUTING FOLLOW SETS")
    print("=" * 50)
    for non_terminal in grammar:
        print(f"\n--- Computing FOLLOW({non_terminal}) ---")
        compute_follow(non_terminal, grammar, first_sets, follow_sets, start_symbol)
        print(f"--- FOLLOW({non_terminal}) = {follow_sets[non_terminal]} ---\n")

    # Print Results (non-terminals only)
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print("FIRST sets:")
    for nt in grammar:  # only non-terminals
        print(f"FIRST({nt}) = {first_sets[nt]}")

    print("\nFOLLOW sets:")
    for nt in grammar:  # only non-terminals
        print(f"FOLLOW({nt}) = {follow_sets[nt]}")
    print("=" * 50)

if __name__ == "__main__":
    main()
