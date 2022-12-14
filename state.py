import matplotlib.pyplot as plt
from move import Move
from board import N


class State:
    """Game state in a specific turn."""
    def __init__(self, done_moves, available_moves, player_turn = 1,\
                    players_score = [0,0], ai=False):
        # Done moves and borders
        self.done_moves = done_moves

        # All available moves 
        self.available_moves = available_moves 

        # Turn of the current player [0,1]
        self.player_turn = player_turn

        # Players score
        self.players_score = players_score

        # Is this a future state computed by AI?
        self.ai = ai

    def check_box(self, last_move, orientation):
        """Check if a box was created."""
        # Unpack move
        x1, y1, x2, y2 = last_move.unpack()

        for i in [-1, 1]:
            if orientation == "-":
                a = ((x1, y1+i), (x2, y2+i)) # bb/tt
                b = ((x2, y2), (x2, y2+i)) ## br/tr
                c = ((x1, y1), (x1, y1+i)) ## bl/tl
            else: # orientation == "|"
                a = ((x1+i, y1), (x2+i, y2)) # ll/rr
                b = ((x2, y2), (x2+i, y2)) # lt/rt
                c = ((x1, y1), (x1+i, y1)) # lb/rb

            # Plot a cross in the box (if created)
            if Move(*a).done(self) and Move(*b).done(self) and Move(*c).done(self):
                if not(self.ai):
                    # Plot
                    Move((x1, y1), (a[1][0], a[1][1])).plot(turn = self.player_turn)
                    Move((x2, y2), (a[0][0], a[0][1])).plot(turn = self.player_turn)

                # Increment score of the current player
                self.players_score[self.player_turn] += 1

    def get_win_threshold(self):
        """Get win threshold."""
        max_boxes = (N-1)**2
        return round(max_boxes/2) + 1       

    def evaluate(self):
        """Return evaluation of the position."""
        return self.players_score[1] - self.players_score[0]

    def gameover(self):
        """Return true if the game is over."""
        # Get win threshold
        win_threshold = self.get_win_threshold()

        # Game over conditions
        player1_won = self.players_score[0] >= win_threshold
        player2_won = self.players_score[1] >= win_threshold
        tie = self.evaluate() == 0 and not(self.moves_left())

        if player1_won or player2_won or tie:
            return True
        else:
            return False

    def next_turn(self):
        """Proceed to the next turn."""
        # Check gameover
        if self.gameover():
            scoreboard = "GAME OVER \n\n"
        else:
            # Change player turn
            self.player_turn = not(self.player_turn)
            scoreboard = ""

        # Print scoreboard
        for i in range(2):
            if self.player_turn == i:
                scoreboard += "* "
            else:
                scoreboard += "   "

            scoreboard += "Player {}: {}\n".format(i+1, self.players_score[i])

        plt.title(scoreboard)

    def moves_left(self):
        """Return true if there are remaining moves"""
        return len(self.available_moves) > 0