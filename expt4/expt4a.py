from collections import defaultdict

# Function to compute FIRST set
def compute_first(symbol, grammar, first_sets):
    if symbol in first_sets:
        return first_sets[symbol]
    
    first = set()
    if symbol not in grammar:  # terminal
        first.add(symbol)
    else:
        for production in grammar[symbol]:
            if production == ["ε"]:  # epsilon
                first.add("ε")
            else:
                for char in production:
                    first_char = compute_first(char, grammar, first_sets)
                    first |= (first_char - {"ε"})
                    if "ε" not in first_char:
                        break
                else:
                    first.add("ε")
    first_sets[symbol] = first
    return first

# Function to compute FOLLOW set
def compute_follow(symbol, grammar, first_sets, follow_sets, start_symbol):
    if symbol == start_symbol:
        follow_sets[symbol].add("$")
    
    for lhs in grammar:
        for production in grammar[lhs]:
            for i, char in enumerate(production):
                if char == symbol:
                    # Case 1: next symbol exists
                    if i + 1 < len(production):
                        next_char = production[i+1]
                        next_first = compute_first(next_char, grammar, first_sets)
                        follow_sets[symbol] |= (next_first - {"ε"})
                        if "ε" in next_first:
                            if lhs != symbol:
                                follow_sets[symbol] |= (compute_follow(lhs, grammar, first_sets, follow_sets, start_symbol) - {"ε"})
                    else:
                        if lhs != symbol:
                            follow_sets[symbol] |= (compute_follow(lhs, grammar, first_sets, follow_sets, start_symbol) - {"ε"})
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
    for non_terminal in grammar:
        compute_first(non_terminal, grammar, first_sets)

    # Compute FOLLOW sets for non-terminals only
    for non_terminal in grammar:
        compute_follow(non_terminal, grammar, first_sets, follow_sets, start_symbol)

    # Print Results (non-terminals only)
    print("FIRST sets:")
    for nt in grammar:  # only non-terminals
        print(f"FIRST({nt}) = {first_sets[nt]}")

    print("\nFOLLOW sets:")
    for nt in grammar:  # only non-terminals
        print(f"FOLLOW({nt}) = {follow_sets[nt]}")

if __name__ == "__main__":
    main()
