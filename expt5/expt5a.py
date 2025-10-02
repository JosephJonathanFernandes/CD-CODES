from collections import defaultdict

def eliminate_left_recursion(grammar):
    print("\n" + "="*80)
    print("LEFT RECURSION ELIMINATION ALGORITHM")
    print("="*80)
    
    print("\nFORMULA:")
    print("If we have: A → Aα₁ | Aα₂ | ... | Aαₘ | β₁ | β₂ | ... | βₙ")
    print("Transform to:")
    print("A → β₁A' | β₂A' | ... | βₙA'")
    print("A' → α₁A' | α₂A' | ... | αₘA' | ε")
    print("\nWhere:")
    print("- α represents the part after A in left-recursive productions")
    print("- β represents non-left-recursive productions")
    print("- A' is a new non-terminal")
    print("- ε is epsilon (empty string)")
    
    new_grammar = defaultdict(list)

    for non_terminal in grammar:
        print(f"\n" + "-"*60)
        print(f"PROCESSING NON-TERMINAL: {non_terminal}")
        print("-"*60)
        
        alpha = []  # left recursive parts (α)
        beta = []   # non-left recursive parts (β)

        print(f"\nAnalyzing productions for {non_terminal}:")
        for i, production in enumerate(grammar[non_terminal]):
            prod_str = " ".join(production)
            if production[0] == non_terminal:
                # A → Aα
                alpha_part = production[1:]
                alpha.append(alpha_part)
                alpha_str = " ".join(alpha_part) if alpha_part else "ε"
                print(f"  {non_terminal} → {non_terminal}{alpha_str} [LEFT RECURSIVE - α = '{alpha_str}']")
            else:
                # A → β
                beta.append(production)
                beta_str = " ".join(production)
                print(f"  {non_terminal} → {beta_str} [NON-LEFT RECURSIVE - β = '{beta_str}']")

        print(f"\nCollected α parts: {[' '.join(a) if a else 'ε' for a in alpha]}")
        print(f"Collected β parts: {[' '.join(b) for b in beta]}")

        if alpha:
            print(f"\n🔄 LEFT RECURSION DETECTED! Applying transformation...")
            new_nt = non_terminal + "'"
            print(f"Creating new non-terminal: {new_nt}")
            
            print(f"\nStep 1: Transform {non_terminal} productions")
            print(f"Formula: {non_terminal} → β₁{new_nt} | β₂{new_nt} | ... | βₙ{new_nt}")
            for i, b in enumerate(beta):
                new_prod = b + [new_nt]
                new_grammar[non_terminal].append(new_prod)
                beta_str = " ".join(b)
                new_prod_str = " ".join(new_prod)
                print(f"  β{i+1} = '{beta_str}' → {non_terminal} → {new_prod_str}")
            
            print(f"\nStep 2: Create {new_nt} productions")
            print(f"Formula: {new_nt} → α₁{new_nt} | α₂{new_nt} | ... | αₘ{new_nt} | ε")
            for i, a in enumerate(alpha):
                new_prod = a + [new_nt]
                new_grammar[new_nt].append(new_prod)
                alpha_str = " ".join(a) if a else "ε"
                new_prod_str = " ".join(new_prod)
                print(f"  α{i+1} = '{alpha_str}' → {new_nt} → {new_prod_str}")
            
            # Add epsilon production
            new_grammar[new_nt].append(["ε"])
            print(f"  Adding epsilon: {new_nt} → ε")
            
            print(f"\n✅ Transformation complete for {non_terminal}")
        else:
            print(f"\n✅ No left recursion found for {non_terminal}")
            print(f"Keeping original productions unchanged")
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
        print(f"  {nt} → {' | '.join(rhs)}")
    if not grammar:
        print("  (No productions)")
    print()


# ---------------- MAIN ----------------
def main():
    print("🚀 LEFT RECURSION ELIMINATION DEMONSTRATION")
    print("="*80)
    
    filename = "grammar.txt"
    print(f"\n📖 Reading grammar from: {filename}")
    grammar = read_grammar_from_file(filename)

    print("\n📋 ORIGINAL GRAMMAR:")
    print("="*40)
    print_grammar(grammar)
    
    print(f"\n🔍 CHECKING FOR LEFT RECURSION:")
    print("Left recursion occurs when: A → Aα (A appears as first symbol on RHS)")

    updated_grammar = eliminate_left_recursion(grammar)

    print(f"\n" + "="*80)
    print("🎯 FINAL RESULT - GRAMMAR AFTER ELIMINATING LEFT RECURSION:")
    print("="*80)
    print_grammar(updated_grammar)
    
    print(f"\n📚 SUMMARY:")
    print("- Left recursion has been successfully eliminated")
    print("- New non-terminals with ' (prime) have been introduced")
    print("- The grammar is now suitable for top-down parsing")
    print("- Epsilon (ε) productions handle the recursive nature")


if __name__ == "__main__":
    main()
