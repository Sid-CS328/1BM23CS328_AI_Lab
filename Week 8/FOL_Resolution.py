# Create a knowledge base consisting of first order logic statements and prove the given query using Resolution


from itertools import combinations

def negate(literal):
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal

def is_variable(x):
    return isinstance(x, str) and len(x) == 1 and x.islower()

def get_predicate(literal):
    if literal.startswith("~"):
        return literal[1:literal.find("(")]
    else:
        return literal[:literal.find("(")]

def get_args_from_literal(literal):
    return [arg.strip() for arg in literal[literal.find("(")+1:-1].split(",")]

def literal_to_tuple(literal):
    pred = get_predicate(literal)
    args = get_args_from_literal(literal)
    return (pred, *args)

def tuple_to_literal(tuple_form, negated=False):
    pred = tuple_form[0]
    args = ", ".join(tuple_form[1:])
    literal = f"{pred}({args})"
    if negated:
        return "~" + literal
    else:
        return literal

def substitute_literal(literal, subs):
    lit_tuple = literal_to_tuple(literal)
    new_args = []
    for arg in lit_tuple[1:]:
        if is_variable(arg) and arg in subs:
            new_args.append(subs[arg])
        else:
            new_args.append(arg)
    new_literal_tuple = (lit_tuple[0], *new_args)
    return tuple_to_literal(new_literal_tuple, literal.startswith("~"))


def resolve(ci, cj):
    resolvents = set()
    for lit_i in ci:
        for lit_j in cj:
            if negate(lit_i) == lit_j or lit_i == negate(lit_j):
                new_clause = (ci - {lit_i}) | (cj - {lit_j})
                resolvents.add(frozenset(new_clause))

    for lit_i in ci:
        for lit_j in cj:
            neg_lit_i = negate(lit_i)
            if get_predicate(neg_lit_i) == get_predicate(lit_j) and len(get_args_from_literal(neg_lit_i)) == len(get_args_from_literal(lit_j)):
                term_i = literal_to_tuple(neg_lit_i)
                term_j = literal_to_tuple(lit_j)

                unifier = unify(term_i, term_j)

                if unifier != "failure":
                    new_clause_i = {substitute_literal(l, unifier) for l in ci - {lit_i}}
                    new_clause_j = {substitute_literal(l, unifier) for l in cj - {lit_j}}
                    new_clause = frozenset(new_clause_i | new_clause_j)
                    resolvents.add(new_clause)

    return resolvents

def resolution(kb, query):
    kb_clauses = set(kb)
    kb_clauses.add(frozenset([negate(query)]))

    new_clauses = set()
    iterations = 0

    while True:
        iterations += 1
        print(f"\nIteration {iterations}: KB size = {len(kb_clauses)}")
        pairs = list(combinations(kb_clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for res in resolvents:
                if frozenset() in resolvents:
                    print("\nDerived empty clause -> Contradiction found")
                    return True
                if res not in kb_clauses and res not in new_clauses:
                    new_clauses.add(res)

        if new_clauses.issubset(kb_clauses):
            return False
        kb_clauses = kb_clauses.union(new_clauses)
        new_clauses = set()


def is_variable(x):
    return isinstance(x, str) and len(x) == 1 and x.islower()

def is_compound(x):
    return isinstance(x, tuple) and len(x) > 0

def get_functor(x):
    return x[0] if is_compound(x) else None

def get_args(x):
    return list(x[1:]) if is_compound(x) else []

def occur_check(var, x, theta):
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    elif is_compound(x):
        return any(occur_check(var, arg, theta) for arg in get_args(x))
    else:
        return False

def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if theta == "failure":
        return "failure"
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif is_compound(x) and is_compound(y):
        if get_functor(x) != get_functor(y):
            return "failure"
        if len(get_args(x)) != len(get_args(y)):
            return "failure"
        return unify(get_args(x), get_args(y), theta)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return "failure"
        if not x:
            return theta
        first_unify = unify(x[0], y[0], theta)
        if first_unify == "failure":
            return "failure"
        return unify(x[1:], y[1:], first_unify)
    else:
        return "failure"

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    elif occur_check(var, x, theta):
        return "failure"
    else:
        theta[var] = x
        return theta


kb = set()

kb.add(frozenset(["~Food(x)", "Likes(John, x)"]))
kb.add(frozenset(["Food(Peanuts)"]))
kb.add(frozenset(["Food(Apple)"]))
kb.add(frozenset(["Food(Vegetables)"]))
kb.add(frozenset(["~Eats(x, y)", "Killed(x)", "Food(y)"]))
kb.add(frozenset(["Eats(Anil, Peanuts)"]))
kb.add(frozenset(["Alive(Anil)"]))
kb.add(frozenset(["~Eats(Anil, y)", "Eats(Harry, y)"]))
kb.add(frozenset(["~Alive(x)", "~Killed(x)"]))
kb.add(frozenset(["Killed(x)", "Alive(x)"]))


print("Knowledge Base (Clauses):")
for c in kb:
    print(c)

query = "Likes(John, Peanuts)"

proved = resolution(kb, query)

print("\nResult:")
if proved:
    print(f"Query proved: {query}")
else:
    print(f"Could not prove the query: {query}")


print()
print("Name: Siddharth Arya")
print("USN: 1BM23CS328")
