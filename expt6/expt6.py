# Predictive Parser Implementation in Python

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
                if len(prod) == 1 and prod[0] == 'ε':
                    if 'ε' not in first[head]:
                        first[head].add('ε')
                        changed = True
                    continue
                # iterate symbols in the production
                add_eps = True
                for s in prod:
                    if s in productions:
                        # non-terminal
                        before = len(first[head])
                        first[head] |= (first[s] - {'ε'})
                        if 'ε' in first[s]:
                            # continue to next symbol
                            pass
                        else:
                            add_eps = False
                            break
                        if len(first[head]) != before:
                            changed = True
                    else:
                        # terminal
                        if s not in first[head]:
                            first[head].add(s)
                            changed = True
                        add_eps = False
                        break
                else:
                    # all symbols can produce epsilon
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
    for head, prods in productions.items():
        for prod in prods:
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
                table[(head, terminal)] = prod
            if 'ε' in first_set:
                for terminal in follow.get(head, set()):
                    table[(head, terminal)] = prod
    return table

# Parsing function
def predictive_parse(input_string, start_symbol, table):
    # Tokenize input string into grammar tokens (e.g. 'id', '+', '*', '(', ')')
    tokens = tokenize(input_string)
    tokens.append('$')
    stack = ['$']
    stack.append(start_symbol)
    i = 0
    print(f"{'Stack':<30}{'Input':<30}{'Action'}")
    while stack:
        top = stack.pop()
        current_input = tokens[i]
        print(f"{''.join(stack)+top:<30}{' '.join(tokens[i:]):<30}", end='')
        if top == current_input == '$':
            print("Accept")
            return True
        elif top == current_input:
            print(f"Match {current_input}")
            i += 1
        elif (top, current_input) in table:
            prod = table[(top, current_input)]
            print(f"Output {top} -> {' '.join(prod)}")
            if not (len(prod) == 1 and prod[0] == 'ε'):
                for symbol in reversed(prod):
                    stack.append(symbol)
        else:
            print("Error")
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

    # Compute FIRST sets (use iterative algorithm to handle left-recursion)
    first = compute_all_firsts(productions)

    # Compute FOLLOW sets
    follow = {}
    for symbol in productions:
        follow = compute_follow(symbol, productions, start_symbol, first, follow)

    # Construct Parsing Table
    table = construct_table(productions, first, follow)

    print(f"Using grammar from: {args.grammar}")
    print(f"Start symbol: {start_symbol}")
    print(f"Input: {input_string}\n")

    # Run parser
    result = predictive_parse(input_string, start_symbol, table)
    print('\nParse result:', 'Accepted' if result else 'Rejected')

    # Note: ops/trace file display was removed per user request.


if __name__ == '__main__':
    main()
