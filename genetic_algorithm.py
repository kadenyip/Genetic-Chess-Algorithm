import chess
import random
import math
import chess.polyglot

population_size = 50
mutation_rate = 0.1
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
        if piece.piece_type == chess.KING:
            continue

        val = piece_values[piece.piece_type - 1]

        if piece.color == color:
            score += val
        else: 
            score -= val
    return score

def choose_move(board, genome, color, depth = 1):
    best_move = None
    best_score = -200.0

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, -math.inf, math.inf, False, genome, color)
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    if best_move is None:
        best_move = random.choice(list(board.legal_moves))

    return best_move

def calculate_fitness(genome):
    board = chess.Board()
    for _ in range(20):
        if board.is_game_over():
            break

        genome_move = choose_move(board, genome, chess.WHITE)
        board.push(genome_move)

        if board.is_game_over():
            break

        black_move = random.choice(list(board.legal_moves))
        board.push(black_move)

    return get_material_score(board, standard_values, chess.WHITE)

def crossover(parent1, parent2):
    midpoint = random.randint(1, 3)
    child = parent1[:midpoint] + parent2[midpoint:]
    return child

def mutate(genome):
    child = list(genome)
    for i in range(5):
        if random.random() < mutation_rate:
            change = random.uniform(-1.0, 1.0)
            child[i] = max(0.1, round(child[i] + change, 2))
    return child

def evolve(population):
    population.sort(key=calculate_fitness, reverse=True)
    next_generation = population[:int(population_size * 0.10)]

    while len(next_generation) < population_size:
        p1 = random.choice(population[:20])
        p2 = random.choice(population[:20])

        child = crossover(p1, p2)
        child = mutate(child)
        next_generation.append(child)
    return next_generation

def minimax(board, depth, alpha, beta, maximizing_player, genome, color):
    # Base Case
    if depth == 0 or board.is_game_over():
        return get_material_score(board, genome, color)
    
    if maximizing_player:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)

            eval = minimax(board, depth - 1, alpha, beta, False, genome, color)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break
        return max_eval

    else: 
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)

            eval = minimax(board, depth - 1, alpha, beta, True, genome, color)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            
            if beta <= alpha: 
                break
        return min_eval
    
