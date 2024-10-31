import random


# Initialize the board with empty spaces
board_values = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
# print(board_values)


def print_board():
    board = (f"   A   B   C\n"
             f"1  {board_values[0][0]} | {board_values[0][1]} | {board_values[0][2]} \n"
             f"  ---+---+---\n"
             f"2  {board_values[1][0]} | {board_values[1][1]} | {board_values[1][2]} \n"
             f"  ---+---+---\n"
             f"3  {board_values[2][0]} | {board_values[2][1]} | {board_values[2][2]} \n")
    print(board)
    return


def play_game():
    new_game = input("Do you want to play a new game? Y/N\n")
    new_game = new_game.upper()
    # Y for a new game, N to exit.
    if new_game == 'N':
        exit(0)
    elif new_game == 'Y':
        # Introduction to the game.
        print("This is the game board, when it's your turn choose a position indicating column and row, ie A1:")
        print_board()

        print("Your marks are: X")  # Player uses X
        print("AI marks are: O\n")  # AI uses O

        # Randomly choose who starts.
        turn = choose_order()
        print(f"The first turn goes to: {turn}\n")

        game_is_over = False

        while game_is_over is False:
            # AI turn
            if turn == "AI":
                ai_turn()   # AI plays
                turn = "Player"     # Change turn
            # Player turn
            elif turn == "Player":
                player_turn()  # AI plays
                turn = "AI"  # Change turn

    else:
        print("Sorry, I don't understand that. type Y for a new game or N to exit.\n")
        play_game()


# Randomly choose which player starts
def choose_order():
    return random.choice(["Player", "AI"])


def ai_turn():
    best_score = float('-inf')
    best_move = None

    print("Current board state before AI's turn:")
    print_board()

    for row in range(3):
        for col in range(3):
            if board_values[row][col] == " ":
                # Try the move
                board_values[row][col] = "O"
                score = minimax(board_values, 0, False)
                board_values[row][col] = " "

                # print(f"Score for placing O at {chr(col + 65)}{row + 1}: {score}")

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        board_values[row][col] = "O"
        print("AI places an 'O' at", chr(col + 65), row + 1)

    else:
        # If there is no best move, pick a random empty cell
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board_values[r][c] == " "]
        if empty_cells:  # Ensure there are empty cells to choose from
            row, col = random.choice(empty_cells)
            board_values[row][col] = "O"
            print("AI places an 'O' at", chr(col + 65), row + 1)  # A1, B2, etc.
    print_board()
    if check_winning():
        print("You've lost to the AI. Try again.\n")
        reset_board()
        play_game()
    if check_draw():
        print("It's a draw. It was close, try again.")
        reset_board()
        play_game()

    return


def minimax(board, depth, is_maximizing):
    if is_maximizing:  # AI's turn
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score

    else:  # Player's turn
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score


def player_turn():
    selection = input("Choose a position indicating column and row, ie A1:")
    selection = selection.upper()

    # Check if selection is valid
    if not validate_selection(sel=selection):
        print("Your selection is invalid, choose a position that is a combination of ABC and 123, ie B2.\n")
        player_turn()

    # Translate selection to index
    row = int(selection[1]) - 1
    column = selection[0]
    if column == "A":
        column = 0
    elif column == "B":
        column = 1
    elif column == "C":
        column = 2

    # Check if selection is not occupied
    if board_values[row][column] != " ":
        print("Your selection is already occupied, choose another place in the board.\n")
        player_turn()

    # Assign selection to player
    board_values[row][column] = "X"
    print(board_values)
    print_board()

    # Check if player has won
    if check_winning():
        print("You have won!!! Congratulations you defeated the AI.\n")
        reset_board()
        play_game()
    if check_draw():
        print("It's a draw. It was close, try again.")
        reset_board()
        play_game()
    return


def check_winning():
    game_ended = False
    # Check rows
    if board_values[0][0] == board_values[0][1] == board_values[0][2] != " ":
        game_ended = True
    elif board_values[1][0] == board_values[1][1] == board_values[1][2] != " ":
        game_ended = True
    elif board_values[2][0] == board_values[2][1] == board_values[2][2] != " ":
        game_ended = True

    # Check columns
    elif board_values[0][0] == board_values[1][0] == board_values[2][0] != " ":
        game_ended = True
    elif board_values[0][1] == board_values[1][1] == board_values[2][1] != " ":
        game_ended = True
    elif board_values[0][2] == board_values[1][2] == board_values[2][2] != " ":
        game_ended = True

    # Check diagonals
    elif board_values[0][0] == board_values[1][1] == board_values[2][2] != " ":
        game_ended = True
    elif board_values[2][0] == board_values[1][1] == board_values[0][2] != " ":
        game_ended = True

    return game_ended


# If all the spaces in the board are used returns true
def check_draw():
    for row in range(3):
        for col in range(3):
            if board_values[row][col] == " ":
                return False
    return True


def validate_selection(sel):
    valid_options = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    for valid_option in valid_options:
        if valid_option == sel:
            return True
    return False


def reset_board():
    for i in range(0, 3):
        for j in range(0, 3):
            board_values[i][j] = " "
    return


# Press the green button in the gutter to run the script.
play_game()
