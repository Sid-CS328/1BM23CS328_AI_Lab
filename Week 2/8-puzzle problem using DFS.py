# 8-puzzle problem using DFS



from collections import deque


goal_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)


valid_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_move(position, move, size=3):
    row, col = position
    new_row, new_col = row + move[0], col + move[1]
    return 0 <= new_row < size and 0 <= new_col < size

def get_new_state(state, position, move):
    row, col = position
    new_row, new_col = row + move[0], col + move[1]
    new_state = list(state)
    new_pos = new_row * 3 + new_col
    blank_pos = row * 3 + col
    new_state[blank_pos], new_state[new_pos] = new_state[new_pos], new_state[blank_pos]
    return tuple(new_state)

def dfs(start_state):
    stack = [(start_state, start_state.index(0))]
    visited = set()
    visited.add(start_state)
    parent_map = {start_state: None}
    move_map = {start_state: None}

    total_cost = 1

    visited_states = []

    while stack:
        current_state, blank_pos = stack.pop()

        visited_states.append(current_state)

        if current_state == goal_state:
            path = []
            while current_state != start_state:
                path.append(move_map[current_state])
                current_state = parent_map[current_state]
            return path[::-1], visited_states, total_cost
        row, col = divmod(blank_pos, 3)

        for move in valid_moves:
            if is_valid_move((row, col), move):
                new_state = get_new_state(current_state, (row, col), move)
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, new_state.index(0)))
                    parent_map[new_state] = current_state
                    move_map[new_state] = move
                    total_cost += 1 

    return None, visited_states, total_cost

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])


start_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)
print("Start State:")
print_state(start_state)

path, visited_states, total_cost = dfs(start_state)

if path:
    print("\nSolution Path:")
    current_state = start_state
    for move in path:
        print(f"Move blank {move} from {current_state}")
        row, col = divmod(current_state.index(0), 3)
        current_state = get_new_state(current_state, (row, col), move)
        print_state(current_state)
else:
    print("\nNo solution found.")

print("\nVisited States:")
for state in visited_states:
    print_state(state)
    print("----")

print(f"\nTotal Cost (Visited States): {total_cost}")

print("Name: Siddharth Arya")
print("USN: 1BM23CS328")
