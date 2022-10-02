import matplotlib.pyplot as plt
from move import Move

# Board dimension
N = 5


def plot():
    """Plot game board."""
    # Set plot layout 
    plt.tight_layout(pad=5)
    plt.axis("off")

    done_moves = []
    available_moves = []

    for i in range(1, N+1):
        for j in range(1, N):
            # Define linestyle
            ls = "-" if i == N or i == 1 else ":"

            # Define moves
            move1 = Move((i, j), (i, j+1))
            move2 = Move((j, i), (j+1, i))

            # Plot moves
            move1.plot(ls=ls)
            move2.plot(ls=ls)

            if ls == "-":
                # Save square borders as done moves
                done_moves.append(move1)
                done_moves.append(move2)
            else:
                # Save available moves
                available_moves.append(move1)
                available_moves.append(move2)
    
    return done_moves, available_moves