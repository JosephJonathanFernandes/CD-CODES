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

# Sample Grammar
# E -> T E'
# E' -> + T E' | ε
# T -> F T'
# T' -> * F T' | ε
# F -> ( E ) | id

productions = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

start_symbol = 'E'

# Compute FIRST sets
first = {}
for symbol in productions:
    first[symbol] = compute_first(symbol, productions, first)

# Compute FOLLOW sets
follow = {}
for symbol in productions:
    follow = compute_follow(symbol, productions, start_symbol, first, follow)

# Construct Parsing Table
table = construct_table(productions, first, follow)

# Input String
input_string = "id+id*id"

# Parse Input
predictive_parse(input_string, start_symbol, table)
