def prop_fc_ask(kb_facts, kb_rules, query):
    inferred = set(kb_facts)
    new_inferred_something = True
    iteration = 0

    print(f"Initial facts: {inferred}")

    while new_inferred_something:
        iteration += 1
        new_inferred_something = False
        print(f"\nIteration {iteration}:")
        for premises, conclusion in kb_rules:
            all_premises_true = True
            for premise in premises:
                if premise not in inferred:
                    all_premises_true = False
                    break

            if all_premises_true:
                if conclusion not in inferred:
                    inferred.add(conclusion)
                    new_inferred_something = True
                    print(f"  Rule '{' ^ '.join(premises)} -> {conclusion}' fired. Inferred: '{conclusion}'.")

                    if conclusion == query:
                        print(f"\nQuery '{query}' has been proven!")
                        return True
        print(f"  Facts after iteration {iteration}: {inferred}")

    print(f"\nQuery '{query}' could not be proven after {iteration} iterations.")
    return False

initial_facts = {"B", "D", "E"}

rules = [
    ({"B", "C"}, "A"),
    ({"D", "E"}, "C")
]

query = "A"


result = prop_fc_ask(initial_facts, rules, query)

if result:
    print(f"\nConclusion: The query '{query}' is TRUE.")
else:
    print(f"\nConclusion: The query '{query}' is FALSE.")
