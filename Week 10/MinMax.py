# Min - Max Algorithm

import math

class Node:
    def __init__(self, value=None, children=None, is_max=True):
        self.value = value
        self.children = children or []
        self.is_max = is_max

def minimax(node):
    if not node.children:
        return node.value
    
    child_values = [minimax(child) for child in node.children]
    node.value = max(child_values) if node.is_max else min(child_values)
    return node.value

def print_tree(node, level=0):
    indent = "   " * level
    if not node.children:
        print(f"{indent}Leaf Node (value={node.value})")
    else:
        role = "MAX" if node.is_max else "MIN"
        print(f"{indent}{role} Node (value={node.value})")
        for child in node.children:
            print_tree(child, level + 1)

def build_tree_from_leaves(leaf_values, branching_factor, is_max=True):
    current_level_nodes = [Node(value=v, is_max=not is_max) for v in leaf_values]
    level = 1

    while len(current_level_nodes) > 1:
        next_level_nodes = []
        for i in range(0, len(current_level_nodes), branching_factor):
            children = current_level_nodes[i:i + branching_factor]
            node = Node(children=children, is_max=(level % 2 == 0))
            next_level_nodes.append(node)
        current_level_nodes = next_level_nodes
        level += 1

    root = current_level_nodes[0]
    root.is_max = True
    return root


if __name__ == "__main__":
    print("=== Generalized Minimax Tree ===")
    branching_factor = int(input("Enter number of branches per node: "))
    num_leaves = int(input("Enter total number of leaf nodes: "))


    depth = math.log(num_leaves, branching_factor) + 1
    if abs(round(depth) - depth) > 1e-9:
        print("\n Error: The number of leaves must form a full tree (b^(d-1)).")
        print("   For example, with 3 branches per node, leaf count could be 3, 9, 27, etc.")
        exit()

    depth = int(round(depth))
    print(f"\n Tree depth will be {depth} levels (including root).")

    leaf_values = []
    print("\nEnter the values for each leaf node (can be number, inf, -inf):")
    for i in range(num_leaves):
        val = input(f"Leaf {i+1}: ").strip()
        if val.lower() == "inf":
            val = math.inf
        elif val.lower() == "-inf":
            val = -math.inf
        else:
            val = float(val)
        leaf_values.append(val)

    root = build_tree_from_leaves(leaf_values, branching_factor, is_max=True)
    best_value = minimax(root)

    print("\n=== Minimax Result ===")
    print(f"Best value for root: {best_value}\n")

    print("=== Game Tree ===")
    print_tree(root)

