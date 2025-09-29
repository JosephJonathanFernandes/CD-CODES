from collections import defaultdict

def eliminate_left_recursion(grammar):
    new_grammar = defaultdict(list)

    for non_terminal in grammar:
        alpha = []  # left recursive parts
        beta = []   # non-left recursive parts

        for production in grammar[non_terminal]:
            if production[0] == non_terminal:
                # A → Aα
                alpha.append(production[1:])
            else:
                # A → β
                beta.append(production)

        if alpha:
            new_nt = non_terminal + "'"
            for b in beta:
                new_grammar[non_terminal].append(b + [new_nt])
            for a in alpha:
                new_grammar[new_nt].append(a + [new_nt])
            new_grammar[new_nt].append(["ε"])  # epsilon
        else:
            new_grammar[non_terminal].extend(beta)

    return new_grammar


def read_grammar_from_file(filename):
    grammar = defaultdict(list)
    with open(filename, "r") as f:
        for line in f:
            if "->" in line:
                lhs, rhs = line.strip().split("->")
                lhs = lhs.strip()
                productions = rhs.strip().split("|")
                for prod in productions:
                    grammar[lhs].append(prod.strip().split())
    return grammar


def print_grammar(grammar):
    for nt in grammar:
        rhs = [" ".join(p) for p in grammar[nt]]
        print(f"{nt} -> {' | '.join(rhs)}")


# ---------------- MAIN ----------------
def main():
    filename = "grammar.txt"
    grammar = read_grammar_from_file(filename)

    print("Original Grammar:")
    print_grammar(grammar)

    updated_grammar = eliminate_left_recursion(grammar)

    print("\nGrammar after Eliminating Left Recursion:")
    print_grammar(updated_grammar)


if __name__ == "__main__":
    main()
