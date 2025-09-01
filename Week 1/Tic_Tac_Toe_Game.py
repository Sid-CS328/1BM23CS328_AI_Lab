# Tic-Tac-Toe game



import random


board = [' ' for _ in range(9)]  
current_winner = None 


def print_board():
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")


def check_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw():
    return ' ' not in board

def available_moves():
    return [i for i, spot in enumerate(board) if spot == ' ']

def make_move(position, player):
    if board[position] == ' ':
        board[position] = player
        return True
    return False

def computer_move():
    return random.choice(available_moves())


def play_game():
    global current_winner

    print_board()

    user_player = 'X'
    computer_player = 'O'

    while True:
        user_move = int(input("Enter your move (0-8): "))
        if make_move(user_move, user_player):
            print("Player (X) moves:")
            print_board()

            if check_winner(user_player):
                current_winner = user_player
                print("You win!")
                break

            if check_draw():
                print("It's a draw!")
                break

            computer_move_position = computer_move()
            make_move(computer_move_position, computer_player)
            print("Computer's move:")
            print_board()

            if check_winner(computer_player):
                current_winner = computer_player
                print("Computer wins!")
                break

            if check_draw():
                print("It's a draw!")
                break
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    play_game()
