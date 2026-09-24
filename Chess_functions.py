import chess
import random
import chess.svg
from stockfish import Stockfish

# Chess board intialization and the string is the ID for the starting positions
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# Stockfish initialization to recieve data on the current game evaluation
# Use the raw string 'r' prefix so Windows backslashes don't cause errors
engine = Stockfish(
    path=r"C:\Users\Andy\Downloads\stockfish\stockfish-windows-x86-64-universal.exe", 
    depth=10, 
    parameters={
        "Threads": 2, 
        "Hash": 500,         
        "Skill Level": 20,        
        "Minimum Thinking Time": 2 
    }
)

def save_board_svg(filename="board.svg"):
    svg_data = chess.svg.board(board)
    with open(filename, "w") as f:
        f.write(svg_data)

def get_legal_moves():
    return board.legal_moves

def make_move(move_str):
    try:
        move = board.parse_san(move_str)
        if move in board.legal_moves:
            board.push(move)
            save_board_svg()
            print(f"\nMove {move_str} played successfully.")
            return True
    except ValueError:
        pass

    print(f"Move {move_str} is illegal.")
    return False

def is_checkmate():
    return board.is_checkmate()

def computer_move():
    legal_list = list(board.legal_moves)

    # If there are no more legal moves, prevent from crashing
    if not legal_list:
        return False

    chosen_move = random.choice(legal_list)

    move_str = board.san(chosen_move)
    print(f"Computer chose the move {move_str}.")
    return make_move(move_str)

def get_current_evaluation():
    # Use FEN in order to allow stockfish to analyze the entire board
    engine.set_fen_position(board.fen())
    eval_info = engine.get_evaluation()

    if eval_info["type"] == "cp":
        score = eval_info["value"] / 100.0
        return round(score, 2)
    elif eval_info("type") == "mate":
        return 100.0
    if eval_info["value"] < 0:
            return -100.0
    return 0.0



save_board_svg()

    
