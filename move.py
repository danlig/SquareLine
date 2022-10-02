import matplotlib.pyplot as plt

class Move:
    """Define 'move' object."""
    def __init__(self, d1, d2):
        self.dots = {d1, d2}

    def get(self):
        """Get set of dots representing the move."""
        return self.dots

    def unpack(self):
        """Get dots coordinates of a move."""
        # Get dots
        d1, d2 = self.get()

        # Get dots coordinates
        x1, y1 = d1
        x2, y2 = d2

        return x1, y1, x2, y2

    def done(self, state):
        """Check if a move was already done."""
        return self.dots in [m.dots for m in state.done_moves]

    def plot(self, ls="-", c="black", turn=-1):
        """Plot a move."""
        # Unpack move
        x1, y1, x2, y2 = self.unpack()

        # Set specific color for players
        if(turn == 0):
            c = "blue"
        elif (turn == 1):
            c = "red"

        # Plot
        plt.plot([x1, x2], [y1, y2], linestyle = ls, color=c)

    def make(self, state):
        """Make a move, if legal."""
        # Unpack move
        x1, y1, x2, y2 = self.unpack()

        # Check if move is legal
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        delta = delta_x + delta_y

        if delta != 1:
            return 0

        # Check if move was already done
        if self.done(state):
            return 0

        # Link dots and save move
        if not(state.ai):
            self.plot(turn = state.player_turn)
        state.done_moves.append(self)

        # Remove move from available moves list
        for m in state.available_moves:
            if m.dots == self.dots:
                state.available_moves.remove(m)
                break

        # Check if link segment is horizontal or vertical
        orientation = "|" if delta_x == 0 else "-" 
        # Check if a box was created
        state.check_box(self, orientation)

        return 1