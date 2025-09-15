# All steps for Hill Climbing Algorithm

import random

def calculate_cost(board):

    cost = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                cost += 1
    return cost

def get_neighbors(board):
    neighbors = []
    n = len(board)
    for row in range(n):
        for new_col in range(n):
            if new_col != board[row]: 
                new_board = board[:]
                new_board[row] = new_col
                neighbors.append(new_board)
    return neighbors

def hill_climbing(n, max_restarts=100):
    solutions = set()
    all_iterations = []

    for restart in range(max_restarts):
        current_board = [random.randint(0, n-1) for _ in range(n)] 
        current_cost = calculate_cost(current_board)
        iterations = []  

        iterations.append((list(current_board), current_cost))

        while current_cost > 0: 
            neighbors = get_neighbors(current_board)
            next_board = None
            next_cost = current_cost
            
            for neighbor in neighbors:
                cost = calculate_cost(neighbor)
                if cost < next_cost:
                    next_board = neighbor
                    next_cost = cost
            
            if next_board is None:
                break
            else:
                current_board = next_board
                current_cost = next_cost
            
            iterations.append((list(current_board), current_cost))
        
        if current_cost == 0: 
            solutions.add(tuple(current_board)) 
        
        all_iterations.append(iterations)

    return list(solutions), all_iterations

def print_solution(board):
    print(" ".join(map(str, board)))  

n = 4
solutions, all_iterations = hill_climbing(n)

print("Name: Siddharth Arya")
print("USN: 1BM23CS328")

for restart_idx, iterations in enumerate(all_iterations):
    print(f"Restart {restart_idx + 1}:")
    for step_idx, (board_state, cost) in enumerate(iterations):
        print(f"Iteration {step_idx + 1}:")
        print_solution(board_state) 
        print(f"Cost: {cost}")
        print()


for i, solution in enumerate(solutions):
    print(f"Solution {i + 1}:")
    print_solution(solution)  
    print()  
