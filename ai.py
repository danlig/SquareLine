import copy
import random

# Max depth
MAX_DEPTH = 3

# Initial values of Alpha and Beta
MAX_EVAL = +10000000
MIN_EVAL = -10000000


def minimax(state, depth, alpha, beta):
    # Terminating conditions
    # (game over or max depth is reached)
    if (state.gameover()[0] or depth == MAX_DEPTH):
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
    best_move = None
    best_val = MIN_EVAL if state.player_turn else MAX_EVAL

    # Randomize position of available moves 
    # (for more variance in the choice of even evaluation moves)
    random.shuffle(state.available_moves)

    # Evaluate all possible moves
    for move in state.available_moves:
        # Compute evaluation for current move
        future_state = get_future_state(state, move)
        eval = minimax(future_state, 0, MIN_EVAL, MAX_EVAL)

        # Update best move
        if state.player_turn: is_best_move = eval > best_val
        else: is_best_move = eval < best_val

        if (is_best_move):		
            best_move = move
            best_val = eval

    # If there are not best moves, choose a random one
    if best_move == None:
        print("AI selected a random move because no one is good!")
        best_move = random.choice(state.available_moves)

    return best_move