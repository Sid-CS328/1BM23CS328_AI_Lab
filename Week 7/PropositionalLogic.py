# Knowledge Base using Prepositional Logic

# Symbols: AND, OR, Negation/NOT, Implies/Implication, If and only If

from itertools import product

def AND(p, q):
    return p and q

def OR(p, q):
    return p or q

def NOT(p):
    return not p

def IMPLIES(p, q):
    return (not p) or q

def IFF(p, q):
    return p == q

class Formula:
    def __init__(self, op, *args):
        self.op = op
        self.args = args
    
    def evaluate(self, assignment):
        if isinstance(self.op, str) and len(self.args) == 0:
            return assignment[self.op]

        if self.op == 'AND':
            return AND(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'OR':
            return OR(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'NOT':
            return NOT(self.args[0].evaluate(assignment))
        elif self.op == 'IMPLIES':
            return IMPLIES(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'IFF':
            return IFF(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        else:
            raise ValueError(f"Unknown operator: {self.op}")

    def __str__(self):
        if isinstance(self.op, str) and len(self.args) == 0:
            return self.op
        elif self.op == 'NOT':
            return f"¬{self.args[0]}"
        elif self.op == 'AND':
            return f"({self.args[0]} ∧ {self.args[1]})"
        elif self.op == 'OR':
            return f"({self.args[0]} ∨ {self.args[1]})"
        elif self.op == 'IMPLIES':
            return f"({self.args[0]} → {self.args[1]})"
        elif self.op == 'IFF':
            return f"({self.args[0]} ↔ {self.args[1]})"
        else:
            return f"UnknownOp({self.op})"

def extract_symbols(formula):
    symbols = set()
    if isinstance(formula.op, str) and len(formula.args) == 0:
        symbols.add(formula.op)
    else:
        for arg in formula.args:
            symbols |= extract_symbols(arg)
    return symbols

def extract_main_subformulas(formula):
    subs = set()
    subs.add(formula)
    for arg in formula.args:
        subs.add(arg)
    return subs

def entails(KB, alpha):
    base_symbols = {'A', 'B', 'C'}
    symbols_in_formulas = extract_symbols(KB) | extract_symbols(alpha)
    all_symbols = sorted(list(base_symbols | symbols_in_formulas))

    subformulas_KB = extract_subformulas(KB)
    subformulas_alpha = extract_subformulas(alpha)
    all_subformulas = list(subformulas_KB | subformulas_alpha)

    all_subformulas = [f for f in all_subformulas if not (isinstance(f.op, str) and len(f.args) == 0)]

    all_subformulas.sort(key=lambda f: str(f))

    print("Knowledge Base (KB):", KB)
    print("Alpha (Query):", alpha)
    print()

    headers = all_symbols + [str(f) for f in all_subformulas] + ["KB", "Alpha"]

    truth_table = []
    true_assignments = []

    for values in product([False, True], repeat=len(all_symbols)):
        assignment = dict(zip(all_symbols, values))

        subformula_values = []
        for f in all_subformulas:
            val = f.evaluate(assignment)
            subformula_values.append(val)

        kb_val = KB.evaluate(assignment)
        alpha_val = alpha.evaluate(assignment)

        truth_table.append((assignment, subformula_values, kb_val, alpha_val))
        if kb_val and alpha_val:
            true_assignments.append(assignment)

    header_str = " | ".join(f"{h:^12}" for h in headers)
    print(header_str)
    print("-" * len(header_str))

    for assignment, sub_vals, kb_val, alpha_val in truth_table:
        vals = ['T' if assignment[s] else 'F' for s in all_symbols]
        vals += ['T' if v else 'F' for v in sub_vals]
        vals += ['T' if kb_val else 'F', 'T' if alpha_val else 'F']

        row_str = " | ".join(f"{v:^12}" for v in vals)
        print(row_str)

    print("\nAssignments where both KB and Alpha are TRUE:")
    if true_assignments:
        for a in true_assignments:
            print({k: ('T' if v else 'F') for k, v in a.items()})
    else:
        print("None")

    for assignment, sub_vals, kb_val, alpha_val in truth_table:
        if kb_val and not alpha_val:
            print("\nResult: KB does NOT entail Alpha.")
            return False

    print("\nResult: KB entails Alpha.")
    return True



A = Formula('A')
B = Formula('B')
C = Formula('C')

KB = Formula('IFF',
             Formula('IMPLIES',
                     Formula('AND', A, Formula('NOT', B)),
                     Formula('OR', C, A)),
             Formula('OR', B, Formula('NOT', C))
            )

alpha = Formula('IMPLIES', A, C)

result = entails(KB, alpha)
print(f"\nDoes KB entail alpha? {result}")

print("Name: Siddharth Arya")
print("USN: 1BM23CS328")

