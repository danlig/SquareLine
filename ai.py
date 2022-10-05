import copy
import random
import numpy
from functools import partial
from multiprocessing import Pool

# Max depth
MAX_DEPTH = 3

# Initial values of Alpha and Beta
MAX_EVAL = +10000000
MIN_EVAL = -10000000


def minimax(state, depth, alpha, beta):
    # Terminating conditions
    # (game over or max depth is reached)
    if (state.gameover() or depth == MAX_DEPTH):
        return state.evaluate()

    # Maximizer's turn (player 2)
    if state.player_turn:
        best = MIN_EVAL

        # Evaluate all possible moves
        for move in state.available_moves:
            future_state = get_future_state(state, move)

            val = minimax(future_state, depth+1, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
 
            # Alpha Beta Pruning
            if beta <= alpha:
                break
          
        return best

	# Minimizer's turn (player 1)
    else:
        best = MAX_EVAL

        # Make all possible moves
        for move in state.available_moves:
            future_state = get_future_state(state, move)

            val = minimax(future_state, depth+1, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
 
            # Alpha Beta Pruning
            if beta <= alpha:
                break
		
        return best

def get_future_state(current_state, move):
    """Get future state after making a move."""
    # Make new game state
    future_state = copy.deepcopy(current_state)
    future_state.ai = True

    # Make the move
    move.make(future_state)

    # Change turn
    future_state.player_turn = not(future_state.player_turn)

    return future_state

def find_best_move(state):
    """This will return the best possible move for the player"""
    # Randomize position of available moves 
    # (for more variance in the choice of even evaluation moves)
    random.shuffle(state.available_moves)

    global evaluate_move
    def evaluate_move(move, s):
        """Compute evaluation of a move."""
        return minimax(get_future_state(s, move), 0, MIN_EVAL, MAX_EVAL)

    # Get evaluation of all possible moves (with multiprocessing)
    p = Pool(len(state.available_moves))
    f = partial(evaluate_move, s=state)
    eval_array = numpy.asarray(p.map(f, state.available_moves))

    if state.player_turn:
        # player 2 (maximizer)
        best_val = numpy.amax(eval_array)
        i = numpy.argmax(eval_array)
    else:
        # player 1 (minimizer)
        best_val = numpy.amin(eval_array)
        i = numpy.argmin(eval_array)

    # Print best move evaluation
    print("Best move done (depth: {}), evaluation: {}"\
        .format(MAX_DEPTH, best_val))

    return state.available_moves[i]