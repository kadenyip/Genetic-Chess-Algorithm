import chess
import random

population_size = 50
mutation_rate = 50
generations = 20

# In chess, pawn = 1.0, knights = 3.0, bishops = 3.0
# rooks = 5.0 and queens = 9.0
standard_values = [1.0, 3.0, 3.0, 5.0, 9.0]

def random_genome():
    """
    This function will generate completely random values for the 5 main
    chess pieces and it will round it to 2 decimal places.
    """
    return [round(random.uniform(0.5, 10), 2) for _ in range(5)]

def get_material_score(board, piece_values, color):
    score = 0.0
    for square, piece in board.piece_map().items():
