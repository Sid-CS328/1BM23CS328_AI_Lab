# A* algorithm using Misplaced tiles with cost increment

import heapq


GOAL_STATE = (1, 2, 3, 8, 0, 4, 7, 6, 5)
START_STATE = (2, 8, 3, 1, 6, 4, 7, 0, 5)


NEIGHBORS = {
    0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
    3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
    6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
}

def misplaced_tiles(state):
    return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != GOAL_STATE[i])

def get_neighbors(state):
    zero_index = state.index(0)
    neighbors = []
    for swap_index in NEIGHBORS[zero_index]:
        new_state = list(state)
        new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
        neighbors.append(tuple(new_state))
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star_misplaced(start_state):
    open_set = []
    heapq.heappush(open_set, (misplaced_tiles(start_state), 0, start_state))
    came_from = {}
    g_score = {start_state: 0}
    closed_set = set()

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if current == GOAL_STATE:
            return reconstruct_path(came_from, current)

        closed_set.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g = g + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + misplaced_tiles(neighbor)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None

if __name__ == "__main__":
    path = a_star_misplaced(START_STATE)

    if path:
        print("Solution using Misplaced Tiles heuristic:")
        for state in path:
            print(state[:3], state[3:6], state[6:], sep="\n", end="\n\n")
        print(f"Total cost: {len(path) - 1}")
    else:
        print("No solution found.")


    print("Name: Siddharth Arya")
    print("USN: 1BM23CS328")
