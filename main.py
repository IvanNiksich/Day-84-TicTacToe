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
             f"3  {board_values[2][0]} | {board_values[2][1]} | {board_values[2][2]} ")
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


def minimax(board, depth, is_maximizing):
    # Check if the game is over
    if check_winning():
        return 1 if is_maximizing else -1
    elif all(cell != " " for row in board for cell in row):  # Draw
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        # Check for immediate block move
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    if check_winning():
                        board[row][col] = " "
                        return -1  # Prioritize blocking
                    board[row][col] = " "

        # Continue minimax calculation if no immediate block is needed
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score


def ai_turn():
    best_score = float('-inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if board_values[row][col] == " ":
                board_values[row][col] = "O"  # AI's tentative move
                score = minimax(board_values, 0, False)
                board_values[row][col] = " "  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        board_values[row][col] = "O"
        print("\nAI chose:")
        print_board()

    # Check if AI has won
    if check_winning():
        print("AI wins!")
        reset_board()
        play_game()

    return


def player_turn():
    print_board()
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
