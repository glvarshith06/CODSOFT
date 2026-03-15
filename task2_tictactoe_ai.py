# ============================================================
# TASK 2 - TIC-TAC-TOE AI (Minimax + Alpha-Beta Pruning)
# CodSoft AI Internship
# ============================================================

import math

# ── Constants ────────────────────────────────────────────────
HUMAN = "X"
AI    = "O"
EMPTY = " "


# ── Board Utilities ──────────────────────────────────────────

def create_board():
    """Return a fresh 3x3 board."""
    return [[EMPTY] * 3 for _ in range(3)]


def print_board(board):
    """Pretty-print the board."""
    print("\n  1   2   3")
    for i, row in enumerate(board):
        print(f"{i+1} " + " | ".join(row))
        if i < 2:
            print("  ---------")
    print()


def get_empty_cells(board):
    """Return list of (row, col) for all empty cells."""
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]


def check_winner(board, player):
    """Return True if the given player has won."""
    # Rows and columns
    for i in range(3):
        if all(board[i][c] == player for c in range(3)):
            return True
        if all(board[r][i] == player for r in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_draw(board):
    """Return True if the board is full with no winner."""
    return len(get_empty_cells(board)) == 0


def game_over(board):
    return check_winner(board, HUMAN) or check_winner(board, AI) or is_draw(board)


# ── Minimax with Alpha-Beta Pruning ──────────────────────────

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    AI  = maximizing player (O)
    Human = minimizing player (X)
    """
    if check_winner(board, AI):
        return 10 - depth
    if check_winner(board, HUMAN):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for (r, c) in get_empty_cells(board):
            board[r][c] = AI
            score = minimax(board, depth + 1, False, alpha, beta)
            board[r][c] = EMPTY
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break   # Beta cut-off
        return best
    else:
        best = math.inf
        for (r, c) in get_empty_cells(board):
            board[r][c] = HUMAN
            score = minimax(board, depth + 1, True, alpha, beta)
            board[r][c] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break   # Alpha cut-off
        return best


def best_move(board):
    """Find the best move for the AI using Minimax."""
    best_score = -math.inf
    move = None
    for (r, c) in get_empty_cells(board):
        board[r][c] = AI
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            move = (r, c)
    return move


# ── Game Loop ────────────────────────────────────────────────

def human_move(board):
    """Prompt the human for a valid move."""
    while True:
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter col (1-3): ")) - 1
            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == EMPTY:
                return row, col
            else:
                print("⚠️  Invalid move. Cell is either out of range or already taken.")
        except ValueError:
            print("⚠️  Please enter numbers only.")


def play():
    board = create_board()
    print("=" * 40)
    print("   Welcome to Tic-Tac-Toe vs AI 🤖")
    print(f"   You are [{HUMAN}]  |  AI is [{AI}]")
    print("=" * 40)

    # Let human choose who goes first
    choice = input("\nDo you want to go first? (y/n): ").strip().lower()
    human_first = choice == "y"

    turn = HUMAN if human_first else AI

    while not game_over(board):
        print_board(board)

        if turn == HUMAN:
            print("Your turn!")
            r, c = human_move(board)
            board[r][c] = HUMAN
            turn = AI
        else:
            print("AI is thinking... 🤔")
            r, c = best_move(board)
            board[r][c] = AI
            print(f"AI played at row {r+1}, col {c+1}")
            turn = HUMAN

    print_board(board)

    if check_winner(board, HUMAN):
        print("🎉 Congratulations! You won!")
    elif check_winner(board, AI):
        print("🤖 AI wins! Better luck next time.")
    else:
        print("🤝 It's a draw!")


if __name__ == "__main__":
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! 👋")
            break
