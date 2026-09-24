import chess

from chess_logic import (
    save_board_svg,
    make_move,
    get_legal_moves,
    is_checkmate,
    computer_move,
    get_current_evaluation,
    play_opponent_move
)

def main():
    print("Type quit or exit to leave the game")
    while not is_checkmate():
        try:
            user_move = input("Make your move: ")
            if user_move.lower() in ["quit", "exit"]:
                print("Thanks for playing!")
                break

            if make_move(user_move) == False:
                continue

            score = get_current_evaluation()
            print(f"Current Evaluation: {score}\n")

            if is_checkmate():
                print("Checkmate")
                break
            else:
                play_opponent_move()
                score = get_current_evaluation()
                print(f"Current Evaluation: {score}\n")

        except KeyboardInterrupt:
            print("Game forcibly aborted by user input")
            break

if __name__ == "__main__":
    main()
