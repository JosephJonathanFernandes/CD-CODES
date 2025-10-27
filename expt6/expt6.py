# Predictive Parser Implementation in Python
PROD_ARROW = '⇒'  # arrow used when printing productions

# Function to compute FIRST sets
def compute_first(symbol, productions, first):
    # If it's the epsilon symbol
    if symbol == 'ε':
        return {'ε'}
    # If symbol is not a non-terminal (i.e. not a key in productions), it's a terminal
    if symbol not in productions:
        return {symbol}
    result = set()
    for prod in productions.get(symbol, []):
        # prod is a list of symbols
        if len(prod) == 1 and prod[0] == 'ε':
            result.add('ε')
        else:
            for s in prod:
                temp = compute_first(s, productions, first)
                result |= (temp - {'ε'})
                if 'ε' not in temp:
                    break
            else:
                result.add('ε')
    return result


def compute_all_firsts(productions):
    """Compute FIRST sets for all non-terminals using an iterative fixpoint algorithm.

    This is safer than naive recursion for grammars with left recursion.
    """
    first = {nt: set() for nt in productions}
    changed = True
    while changed:
        changed = False
        for head, prods in productions.items():
            for prod in prods:
                # epsilon production
                if len(prod) == 1 and prod[0] == 'ε':
                    if 'ε' not in first[head]:
                        first[head].add('ε')
                        changed = True
                    continue

                # walk symbols in RHS
                all_eps = True
                for sym in prod:
                    if sym not in productions:
                        # terminal
                        if sym not in first[head]:
                            first[head].add(sym)
                            changed = True
                        all_eps = False
                        break
                    else:
                        # non-terminal: add FIRST(sym) minus epsilon
                        before = len(first[head])
                        to_add = first[sym] - {'ε'}
                        if to_add - first[head]:
                            first[head] |= to_add
                            changed = True
                        if 'ε' in first[sym]:
                            # sym can produce epsilon; continue to next symbol
                            continue
                        else:
                            all_eps = False
                            break

                if all_eps:
                    # all symbols can derive epsilon
                    if 'ε' not in first[head]:
                        first[head].add('ε')
                        changed = True

    return first

# Function to compute FOLLOW sets
def compute_follow(symbol, productions, start_symbol, first, follow):
    if symbol not in follow:
        follow[symbol] = set()
    if symbol == start_symbol:
        follow[symbol].add('$')
    for head, prods in productions.items():
        for prod in prods:
            for i, s in enumerate(prod):
                if s == symbol:
                    rest = prod[i+1:]
                    temp = set()
                    if rest:
                        for r in rest:
                            # if r has a FIRST set use it; otherwise r is a terminal
                            if r in first:
                                temp |= (first[r] - {'ε'})
                                if 'ε' not in first[r]:
                                    break
                            else:
                                temp |= {r}
                                break
                        else:
                            temp |= follow.get(head, set())
                    else:
                        temp |= follow.get(head, set())
                    follow[symbol] |= temp
    return follow

# Function to construct predictive parsing table
def construct_table(productions, first, follow):
    table = {}
    origins = {}  # map (A, t) -> "A -> ..." string that added the entry
    conflicts = []
    for head, prods in productions.items():
        for prod in prods:
            prod_str = ' '.join(prod)
            first_set = set()
            if not (len(prod) == 1 and prod[0] == 'ε'):
                for s in prod:
                    if s in first:
                        first_set |= (first[s] - {'ε'})
                        if 'ε' not in first[s]:
                            break
                    else:
                        # s is a terminal
                        first_set |= {s}
                        break
                else:
                    first_set.add('ε')
            else:
                first_set.add('ε')

            for terminal in first_set - {'ε'}:
                key = (head, terminal)
                if key in table and table[key] != prod:
                    conflicts.append((head, terminal, table[key], origins.get(key, ''), prod, f"{head} {PROD_ARROW} {prod_str}"))
                else:
                    table[key] = prod
                    origins[key] = f"{head} {PROD_ARROW} {prod_str}"

            if 'ε' in first_set:
                for terminal in follow.get(head, set()):
                    key = (head, terminal)
                    if key in table and table[key] != prod:
                        conflicts.append((head, terminal, table[key], origins.get(key, ''), prod, f"{head} {PROD_ARROW} {prod_str}"))
                    else:
                        table[key] = prod
                        origins[key] = f"{head} {PROD_ARROW} {prod_str}"

    return table, conflicts, origins


def compute_all_follows(productions, start_symbol, first):
    """Compute FOLLOW sets using an iterative fixpoint algorithm."""
    follow = {nt: set() for nt in productions}
    follow[start_symbol].add('$')
    changed = True
    while changed:
        changed = False
        for head, prods in productions.items():
            for prod in prods:
                for i, B in enumerate(prod):
                    if B not in productions:
                        continue
                    # rest of symbols after B
                    rest = prod[i+1:]
                    # compute FIRST(rest)
                    first_rest = set()
                    if not rest:
                        # add follow(head) to follow(B)
                        before = len(follow[B])
                        follow[B] |= follow[head]
                        if len(follow[B]) != before:
                            changed = True
                    else:
                        add_follow_head = True
                        for sym in rest:
                            if sym in first:
                                before = len(follow[B])
                                follow[B] |= (first[sym] - {'ε'})
                                if len(follow[B]) != before:
                                    changed = True
                                if 'ε' in first[sym]:
                                    # continue to next symbol
                                    continue
                                else:
                                    add_follow_head = False
                                    break
                            else:
                                # sym is terminal
                                before = len(follow[B])
                                follow[B].add(sym)
                                if len(follow[B]) != before:
                                    changed = True
                                add_follow_head = False
                                break
                        if add_follow_head:
                            before = len(follow[B])
                            follow[B] |= follow[head]
                            if len(follow[B]) != before:
                                changed = True
    return follow


def terminals_from_productions(productions):
    terms = set()
    nonterms = set(productions.keys())
    for rhs in productions.values():
        for prod in rhs:
            for sym in prod:
                if sym == 'ε':
                    continue
                if sym not in nonterms:
                    terms.add(sym)
    return sorted(terms)


def pretty_sym(sym):
    # Print symbols as-is; epsilon remains the character 'ε'
    return sym


def print_firsts_and_follows(productions, first, follow):
    nonterms = list(productions.keys())
    print('\nCalculated firsts:')
    for nt in nonterms:
        print(f"first({nt}) => {{{', '.join(sorted(first.get(nt, set())) )}}}")

    print('\nCalculated follows:')
    for nt in nonterms:
        print(f"follow({nt}) => {{{', '.join(sorted(follow.get(nt, set())) )}}}")

    # Nicely formatted table
    print('\nFirsts and Follow Result table\n')
    # prepare column widths
    col1 = max(6, max(len(nt) for nt in nonterms)) + 2
    col2 = max(10, max(len(str(sorted(first.get(nt, set())))) for nt in nonterms) ) + 4
    col3 = max(10, max(len(str(sorted(follow.get(nt, set())))) for nt in nonterms) ) + 4
    # header
    print(f"{ 'Non-T':<{col1}}{ 'FIRST':<{col2}}{ 'FOLLOW':<{col3}}")
    for nt in nonterms:
        fset = sorted(first.get(nt, set()))
        foset = sorted(follow.get(nt, set()))
        print(f"{nt:<{col1}}{str(fset):<{col2}}{str(foset):<{col3}}")


def print_parsing_table(productions, table):
    nonterms = list(productions.keys())
    terms = terminals_from_productions(productions)
    # include $ and ensure unique & keep order
    if '$' not in terms:
        terms = terms + ['$']
    # compute column widths based on content
    col_widths = {}
    # header widths
    col_widths['nonterm'] = max(6, max(len(nt) for nt in nonterms)) + 2
    for t in terms:
        max_cell = len(t)
        for A in nonterms:
            if (A, t) in table:
                prod = table[(A, t)]
                cell = f"{A} {PROD_ARROW} {' '.join(pretty_sym(s) for s in prod)}"
                max_cell = max(max_cell, len(cell))
        col_widths[t] = max_cell + 2

    # print header
    header = f"{'' :<{col_widths['nonterm']}}"
    for t in terms:
        header += f"{t:<{col_widths[t]}}"
    print('\nGenerated parsing table:\n')
    print(header)
    # print rows
    for A in nonterms:
        row = f"{A:<{col_widths['nonterm']}}"
        for t in terms:
            cell = ''
            if (A, t) in table:
                prod = table[(A, t)]
                cell = f"{A} {PROD_ARROW} {' '.join(pretty_sym(s) for s in prod)}"
            row += f"{cell:<{col_widths[t]}}"
        print(row)


# Parsing function
def predictive_parse(input_string, start_symbol, table):
    # Tokenize input string into grammar tokens (space separated tokens expected)
    tokens = tokenize(input_string)
    tokens.append('$')
    stack = ['$']
    stack.append(start_symbol)
    i = 0

    print(f"{'Buffer':<30}{'Stack':<30}{'Action'}")
    while True:
        buffer_str = ' '.join(tokens[i:])
        # display stack with top on the left (reverse of internal list)
        stack_str = ' '.join(reversed(stack))
        # peek top
        top = stack.pop() if stack else None
        current_input = tokens[i] if i < len(tokens) else '$'
        action = ''
        if top == current_input == '$':
            print(f"{buffer_str:<30}{stack_str:<30}{'Accept'}")
            return True
        elif top == current_input:
            action = f"Matched:{current_input}"
            print(f"{buffer_str:<30}{stack_str:<30}{action}")
            i += 1
        elif (top, current_input) in table:
            prod = table[(top, current_input)]
            action = f"T[{top}][{current_input}] = {top} {PROD_ARROW} {' '.join(pretty_sym(s) for s in prod)}"
            print(f"{buffer_str:<30}{stack_str:<30}{action}")
            # push RHS in reverse (unless epsilon)
            if not (len(prod) == 1 and prod[0] == 'ε'):
                for symbol in reversed(prod):
                    stack.append(symbol)
            # after pushing, show updated stack state
            new_stack_str = ' '.join(reversed(stack))
            print(f"{buffer_str:<30}{new_stack_str:<30}{''}")
        else:
            action = 'Error: no rule'
            print(f"{buffer_str:<30}{stack_str:<30}{action}")
            return False



def tokenize(s):
    """Very small tokenizer for the sample grammar: recognizes 'id', operators and parentheses."""
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s.startswith('id', i):
            tokens.append('id')
            i += 2
            continue
        # single char tokens
        if s[i] in ['+', '*', '(', ')']:
            tokens.append(s[i])
            i += 1
            continue
        # unknown sequence (collect as a single token)
        j = i
        while j < len(s) and not s[j].isspace() and s[j] not in ['+', '*', '(', ')']:
            j += 1
        tokens.append(s[i:j])
        i = j
    return tokens

import argparse
import sys


def load_grammar(path):
    """Load grammar from a file.

    Expected simple format (examples present in grammar.txt):
    - Lines starting with # are comments
    - Start: S         (optional; overrides first non-terminal)
    - Input: b a       (optional; input tokens separated by spaces)
    - A -> a b | c     (productions)
    """
    productions = {}
    start_symbol = None
    input_tokens = None
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.lower().startswith('start:'):
                start_symbol = line.split(':', 1)[1].strip()
                continue
            if line.lower().startswith('input:'):
                input_tokens = line.split(':', 1)[1].strip()
                continue
            if '->' in line:
                head, rhs = line.split('->', 1)
                head = head.strip()
                alternatives = [alt.strip() for alt in rhs.split('|')]
                prods = []
                for alt in alternatives:
                    if alt == '' or alt == 'ε' or alt.lower() == 'eps':
                        prods.append(['ε'])
                    else:
                        tokens = alt.split()
                        prods.append(tokens)
                productions.setdefault(head, []).extend(prods)
    # If no start symbol provided, pick first LHS
    if not start_symbol:
        if productions:
            start_symbol = next(iter(productions))
    return productions, start_symbol, input_tokens


def format_productions(productions):
    """Return a human friendly string of the grammar productions."""
    lines = []
    for head, prods in productions.items():
        alts = [' '.join(p) for p in prods]
        lines.append(f"{head} {PROD_ARROW} {' | '.join(alts)}")
    return '\n'.join(lines)


def remove_left_recursion(productions):
    """Remove left recursion (indirect + direct) from the grammar.

    Returns (new_productions, steps) where steps is a list of human-readable
    descriptions of each change performed.
    """
    steps = []
    # Work on a copy
    prods = {nt: [list(p) for p in rhs] for nt, rhs in productions.items()}
    nonterminals = list(prods.keys())

    def make_new_nt(base):
        # append a prime marker; ensure uniqueness
        candidate = base + "'"
        while candidate in prods:
            candidate += "'"
        return candidate

    for i, Ai in enumerate(nonterminals):
        # replace Ai -> Aj α where j < i (indirect left recursion elimination)
        for j in range(i):
            Aj = nonterminals[j]
            new_rhs = []
            changed = False
            for prod in prods[Ai]:
                if prod and prod[0] == Aj:
                    # replace Aj γ with β γ for each Aj -> β
                    rest = prod[1:]
                    for beta in prods[Aj]:
                        new_prod = list(beta) + rest
                        new_rhs.append(new_prod)
                        steps.append(f"In {Ai}: replaced {Ai} {PROD_ARROW} {Aj} {' '.join(rest) if rest else ''} with {Ai} {PROD_ARROW} {' '.join(new_prod)} (expanding {Aj} {PROD_ARROW} {' '.join(beta)})")
                    changed = True
                else:
                    new_rhs.append(prod)
            if changed:
                steps.append(f"After expanding {Aj} in {Ai}, {Ai} productions become: {[' '.join(p) for p in new_rhs]}")
                prods[Ai] = new_rhs

        # now remove direct left recursion for Ai
        alpha = []  # productions where Ai -> Ai α
        beta = []   # productions where Ai -> β (not starting with Ai)
        for prod in prods[Ai]:
            if prod and prod[0] == Ai:
                alpha.append(prod[1:])
            else:
                beta.append(prod)

        if alpha:
            Aip = make_new_nt(Ai)
            steps.append(f"Direct left recursion detected in {Ai}. Creating new non-terminal {Aip} and rewriting productions.")
            # Ai -> beta Aip
            new_Ai_rhs = []
            for b in beta:
                if b == ['ε']:
                    new_Ai_rhs.append([Aip])
                else:
                    new_Ai_rhs.append(list(b) + [Aip])
            prods[Ai] = new_Ai_rhs
            # Aip -> alpha Aip | ε
            prods[Aip] = []
            for a in alpha:
                prods[Aip].append(list(a) + [Aip])
            prods[Aip].append(['ε'])
            steps.append(f"{Ai} rewritten as: {[' '.join(p) for p in prods[Ai]]}")
            steps.append(f"{Aip} productions: {[' '.join(p) for p in prods[Aip]]}")
            # also record the new nonterminal in order list so subsequent iterations can use it
            nonterminals.insert(i+1, Aip)

    return prods, steps


def left_factor(productions):
    """Apply left factoring to the grammar. Returns (new_productions, steps).

    This does a simple factoring: when a non-terminal has two or more
    alternatives that share a common prefix (at least the first symbol),
    it pulls the common prefix into a new non-terminal.
    """
    prods = {nt: [list(p) for p in rhs] for nt, rhs in productions.items()}
    steps = []

    def make_new_nt(base):
        candidate = base + "'"
        while candidate in prods:
            candidate += "'"
        return candidate

    changed = True
    while changed:
        changed = False
        for A, alternatives in list(prods.items()):
            if len(alternatives) < 2:
                continue
            # group by first symbol
            groups = {}
            for prod in alternatives:
                key = prod[0] if prod else 'ε'
                groups.setdefault(key, []).append(prod)

            for key, group in groups.items():
                if len(group) < 2:
                    continue
                # find longest common prefix among these prods
                prefix = []
                for symbols in zip(*group):
                    if all(sym == symbols[0] for sym in symbols):
                        prefix.append(symbols[0])
                    else:
                        break
                if not prefix:
                    continue
                # create new non-terminal
                A_dash = make_new_nt(A)
                steps.append(f"Left factoring on {A}: common prefix {' '.join(prefix)} found; created {A_dash}.")
                # build new alternatives
                new_A_alts = []
                for prod in alternatives:
                    if prod[:len(prefix)] == prefix:
                        # moved under A_dash
                        suffix = prod[len(prefix):]
                        if not suffix:
                            prods.setdefault(A_dash, []).append(['ε'])
                        else:
                            prods.setdefault(A_dash, []).append(suffix)
                    else:
                        new_A_alts.append(prod)
                # A -> prefix A_dash | other_alts
                new_A_alts.append(list(prefix) + [A_dash])
                prods[A] = new_A_alts
                changed = True
                break
            if changed:
                break

    return prods, steps



def read_ops_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description='Predictive parser that loads grammar from a file')
    parser.add_argument('--grammar', '-g', default='grammar.txt', help='Path to grammar file (default: grammar.txt)')
    parser.add_argument('--input-string', '-s', help='Input string to parse (tokens separated by spaces where appropriate). If omitted uses Input: from grammar file')
    parser.add_argument('--input-file', '-i', help='File that contains an Input: line or plain input string')
    args = parser.parse_args(argv)

    productions, start_symbol, input_from_grammar = load_grammar(args.grammar)
    if not productions:
        print(f"No productions loaded from {args.grammar}")
        sys.exit(1)
    if args.input_string:
        input_string = args.input_string
    elif args.input_file:
        # try to read first non-empty line or an Input: line
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # if file contains lines, try to find Input:
            for raw in content.splitlines():
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if line.lower().startswith('input:'):
                    input_string = line.split(':', 1)[1].strip()
                    break
            else:
                # fallback: use entire content as input
                input_string = content
    elif input_from_grammar:
        input_string = input_from_grammar
    else:
        print('No input string provided (use --input-string or provide Input: in grammar file).')
        sys.exit(1)

    # Ensure stdout/stderr use UTF-8 so symbols like 'ε' print correctly on Windows
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        # older Python or streams that don't support reconfigure
        pass

    # Show original grammar
    print(f"Using grammar from: {args.grammar}")
    print(f"Start symbol: {start_symbol}")
    print("Original grammar:\n")
    print(format_productions(productions))
    print('\n')

    # Remove left recursion and show steps
    productions_lr_removed, lr_steps = remove_left_recursion(productions)
    if lr_steps:
        print("--- Left Recursion Removal Steps ---")
        for s in lr_steps:
            print("-", s)
        print('\nGrammar after left recursion removal:\n')
        print(format_productions(productions_lr_removed))
        print('\n')
    else:
        print("No left recursion detected.\n")

    # Apply left factoring and show steps
    productions_factored, lf_steps = left_factor(productions_lr_removed)
    if lf_steps:
        print("--- Left Factoring Steps ---")
        for s in lf_steps:
            print("-", s)
        print('\nGrammar after left factoring:\n')
        print(format_productions(productions_factored))
        print('\n')
    else:
        print("No left factoring needed.\n")

    # Use the transformed grammar from here on
    productions = productions_factored

    # Compute FIRST sets (use iterative algorithm)
    first = compute_all_firsts(productions)

    # Compute FOLLOW sets (iterative)
    follow = compute_all_follows(productions, start_symbol, first)

    # Construct Parsing Table and detect LL(1) conflicts
    table, conflicts, origins = construct_table(productions, first, follow)

    # Print FIRST and FOLLOW nicely
    print_firsts_and_follows(productions, first, follow)

    # Print parsing table
    print_parsing_table(productions, table)
    # Report LL(1) status
    if conflicts:
        print('\nGrammar is NOT LL(1). Conflicts found in parsing table:')
        for (A, t, existing_prod, existing_origin, new_prod, new_origin) in conflicts:
            existing_str = existing_origin or (' '.join(existing_prod))
            new_str = new_origin or (' '.join(new_prod))
            print(f"- Conflict at T[{A}][{t}]: existing -> {existing_str}, new -> {new_str}")
    else:
        print('\nGrammar appears to be LL(1) (no table conflicts detected).')

    print(f"\nInput: {input_string}\n")

    # Run parser (detailed trace)
    result = predictive_parse(input_string, start_symbol, table)
    print('\nParse result:', 'Accepted' if result else 'Rejected')

    # Note: ops/trace file display was removed per user request.


if __name__ == '__main__':
    main()
