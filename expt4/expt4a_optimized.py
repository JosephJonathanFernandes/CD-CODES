from collections import defaultdict

class FirstFollowCalculator:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = {}
        self.follow_sets = defaultdict(set)
        self.first_in_progress = set()  # To handle left recursion
        self.follow_in_progress = set()  # To handle left recursion
        self.computation_steps = []
        
    def log_step(self, message):
        """Log computation steps"""
        self.computation_steps.append(message)
        print(message)
    
    def compute_first(self, symbol):
        """Compute FIRST set with memoization and detailed steps"""
        
        # Check if already computed (memoization)
        if symbol in self.first_sets:
            self.log_step(f"✓ FIRST({symbol}) already computed: {self.first_sets[symbol]}")
            return self.first_sets[symbol]
        
        # Check for left recursion
        if symbol in self.first_in_progress:
            self.log_step(f"⚠ Left recursion detected for {symbol}, returning empty set")
            return set()
        
        self.first_in_progress.add(symbol)
        self.log_step(f"\n🔄 Computing FIRST({symbol})...")
        
        first = set()
        
        # Terminal case
        if symbol not in self.grammar:
            first.add(symbol)
            self.log_step(f"  📝 {symbol} is terminal → FIRST({symbol}) = {{{symbol}}}")
        else:
            # Non-terminal case
            self.log_step(f"  📝 {symbol} is non-terminal with productions: {self.grammar[symbol]}")
            
            for i, production in enumerate(self.grammar[symbol]):
                self.log_step(f"    Production {i+1}: {symbol} → {' '.join(production)}")
                
                if production == ["ε"]:
                    first.add("ε")
                    self.log_step(f"      ✅ Added ε to FIRST({symbol})")
                else:
                    # Process each symbol in the production
                    all_have_epsilon = True
                    for j, char in enumerate(production):
                        self.log_step(f"      🔍 Processing symbol {j+1}: {char}")
                        
                        # Recursive call with memoization
                        first_char = self.compute_first(char)
                        
                        # Add non-epsilon symbols
                        before_size = len(first)
                        first |= (first_char - {"ε"})
                        new_symbols = first - (first - (first_char - {"ε"})) if before_size < len(first) else set()
                        
                        if new_symbols:
                            self.log_step(f"        ➕ Added {new_symbols} from FIRST({char}) to FIRST({symbol})")
                        
                        # Check if epsilon is in FIRST(char)
                        if "ε" not in first_char:
                            self.log_step(f"        🛑 {char} doesn't derive ε, stopping here")
                            all_have_epsilon = False
                            break
                        else:
                            self.log_step(f"        ⏭ {char} can derive ε, continuing...")
                    
                    # If all symbols can derive epsilon, add epsilon
                    if all_have_epsilon:
                        first.add("ε")
                        self.log_step(f"      ✅ All symbols derive ε → Added ε to FIRST({symbol})")
        
        # Store result (memoization)
        self.first_sets[symbol] = first
        self.first_in_progress.remove(symbol)
        self.log_step(f"  ✅ Final FIRST({symbol}) = {first}")
        
        return first
    
    def compute_follow(self, symbol, start_symbol):
        """Compute FOLLOW set with memoization and detailed steps"""
        
        # Initialize if first time
        if symbol not in self.follow_sets:
            self.follow_sets[symbol] = set()
        
        # Check for left recursion
        if symbol in self.follow_in_progress:
            self.log_step(f"⚠ FOLLOW recursion detected for {symbol}, returning current set")
            return self.follow_sets[symbol]
        
        self.follow_in_progress.add(symbol)
        self.log_step(f"\n🔄 Computing FOLLOW({symbol})...")
        
        initial_set = self.follow_sets[symbol].copy()
        
        # Start symbol gets $
        if symbol == start_symbol and "$" not in self.follow_sets[symbol]:
            self.follow_sets[symbol].add("$")
            self.log_step(f"  📝 {symbol} is start symbol → Added $ to FOLLOW({symbol})")
        
        # Look for symbol in all productions
        for lhs in self.grammar:
            for prod_num, production in enumerate(self.grammar[lhs]):
                self.log_step(f"  🔍 Checking: {lhs} → {' '.join(production)}")
                
                for i, char in enumerate(production):
                    if char == symbol:
                        self.log_step(f"    ✓ Found {symbol} at position {i}")
                        
                        # Case 1: There's a symbol after current symbol
                        if i + 1 < len(production):
                            next_symbol = production[i + 1]
                            self.log_step(f"      📍 Next symbol: {next_symbol}")
                            
                            # Get FIRST of next symbol (might trigger computation)
                            if next_symbol not in self.first_sets:
                                self.compute_first(next_symbol)
                            
                            next_first = self.first_sets[next_symbol]
                            before_size = len(self.follow_sets[symbol])
                            self.follow_sets[symbol] |= (next_first - {"ε"})
                            
                            if len(self.follow_sets[symbol]) > before_size:
                                added = (next_first - {"ε"})
                                self.log_step(f"        ➕ Added {added} from FIRST({next_symbol}) to FOLLOW({symbol})")
                            
                            # If FIRST(next_symbol) contains ε, add FOLLOW(lhs)
                            if "ε" in next_first:
                                self.log_step(f"        ⚠ {next_symbol} can derive ε → Need FOLLOW({lhs})")
                                if lhs != symbol:  # Avoid infinite recursion
                                    before_size = len(self.follow_sets[symbol])
                                    follow_lhs = self.compute_follow(lhs, start_symbol)
                                    self.follow_sets[symbol] |= follow_lhs
                                    if len(self.follow_sets[symbol]) > before_size:
                                        added = follow_lhs
                                        self.log_step(f"        ➕ Added {added} from FOLLOW({lhs}) to FOLLOW({symbol})")
                        
                        # Case 2: Symbol is at the end of production
                        else:
                            self.log_step(f"      📍 {symbol} is at end of production")
                            if lhs != symbol:  # Avoid infinite recursion
                                self.log_step(f"        ⚠ Need FOLLOW({lhs})")
                                before_size = len(self.follow_sets[symbol])
                                follow_lhs = self.compute_follow(lhs, start_symbol)
                                self.follow_sets[symbol] |= follow_lhs
                                if len(self.follow_sets[symbol]) > before_size:
                                    added = follow_lhs
                                    self.log_step(f"        ➕ Added {added} from FOLLOW({lhs}) to FOLLOW({symbol})")
        
        self.follow_in_progress.remove(symbol)
        
        # Check if anything was added
        if self.follow_sets[symbol] != initial_set:
            self.log_step(f"  ✅ Updated FOLLOW({symbol}) = {self.follow_sets[symbol]}")
        else:
            self.log_step(f"  ✅ No changes to FOLLOW({symbol}) = {self.follow_sets[symbol]}")
        
        return self.follow_sets[symbol]

def main():
    grammar = defaultdict(list)
    filename = "grammar.txt"

    # Read grammar from file
    print("📖 Reading grammar from file...")
    with open(filename, "r") as f:
        for line in f:
            if "->" in line:
                lhs, rhs = line.strip().split("->")
                lhs = lhs.strip()
                productions = rhs.strip().split("|")
                for prod in productions:
                    prod_symbols = prod.strip().split()
                    prod_symbols = ["ε" if sym.lower() == "epsilon" else sym for sym in prod_symbols]
                    grammar[lhs].append(prod_symbols)

    print(f"📋 Grammar loaded:")
    for nt in grammar:
        for i, prod in enumerate(grammar[nt]):
            print(f"  {nt} → {' '.join(prod)}")

    # Initialize calculator
    calculator = FirstFollowCalculator(grammar)
    start_symbol = list(grammar.keys())[0]

    # Compute FIRST sets
    print("\n" + "="*60)
    print("🎯 COMPUTING FIRST SETS WITH MEMOIZATION")
    print("="*60)
    
    for non_terminal in grammar:
        print(f"\n{'='*20} FIRST({non_terminal}) {'='*20}")
        calculator.compute_first(non_terminal)

    # Compute FOLLOW sets
    print("\n" + "="*60)
    print("🎯 COMPUTING FOLLOW SETS WITH MEMOIZATION")
    print("="*60)
    
    for non_terminal in grammar:
        print(f"\n{'='*20} FOLLOW({non_terminal}) {'='*20}")
        calculator.compute_follow(non_terminal, start_symbol)

    # Final results
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    print("\n🔤 FIRST SETS:")
    for nt in grammar:
        print(f"  FIRST({nt}) = {calculator.first_sets[nt]}")

    print("\n🔤 FOLLOW SETS:")
    for nt in grammar:
        print(f"  FOLLOW({nt}) = {calculator.follow_sets[nt]}")
    
    print("\n📈 COMPUTATION STATISTICS:")
    print(f"  Total FIRST computations avoided by memoization: {len([s for s in calculator.computation_steps if 'already computed' in s])}")
    print(f"  Total computation steps logged: {len(calculator.computation_steps)}")

if __name__ == "__main__":
    main()