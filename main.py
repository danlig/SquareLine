import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from time import sleep, time
from ai import find_best_move
from board import plot, N
from state import State
from move import Move

# Current state
current_state = None

# Figure
figure = plt.figure()

# AI is thinking
thinking = False

# Last dot selected
last_dot = ()


def on_click(event, game_type):
    """Manage click event."""
    # Block if gameover or AI is thinking
    if event.button is MouseButton.LEFT \
            and not(current_state.gameover())\
            and not(thinking):

        # AI vs AI game type
        if game_type == 2: 
            ai_vs_ai()

        # Get clicked dot coordinates
        try:
            x = round(event.xdata)
            y = round(event.ydata)
        except TypeError:
            return

        # Check if selected dot is in valid range
        r = range(1, N+1)
        if x not in r or y not in r:
            return

        # Select a dot or make a move
        global last_dot

        if last_dot == ():
            # Select current dot
            last_dot = (x, y)
        else:
            # Make move
            move = Move(last_dot, (x, y))

            try:
                is_legal_move = move.make(current_state)
            except ValueError:
                is_legal_move = 0

            # Restore defaults value
            last_dot = ()

            # Check if legal move
            if not(is_legal_move):
                return
            
            # Next turn
            current_state.next_turn()

            # Refresh figure
            refresh_figure()

            # AI turn
            if game_type == 1:
                ai_turn()

def refresh_figure():
    """Refresh window."""
    figure.canvas.draw()
    figure.canvas.flush_events()
    plt.draw_all()

def ai_vs_ai():
    """AI vs AI game type."""
    while not(current_state.gameover()):
        ai_turn()
        refresh_figure()
        sleep(1)

def ai_turn():
    """AI turn."""
    start = time()
    print("\nAI is thinking a move...")

    global thinking
    thinking = True

    ai_move = find_best_move(current_state)
    ai_move.make(current_state)

    current_state.next_turn()
    refresh_figure()

    thinking = False

    end = time()
    print("Thinking time: {}s".format(round(end-start, 2)))

def main():
    # Menu
    print("1) Player vs AI (default)")
    print("2) AI vs AI")
    print("3) Player vs Player")

    try:
        choice = int(input("- "))
        if choice not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        choice = 1

    # Plot game board and
    # get square borders (as done moves) and available moves
    done_moves, available_moves = plot()

    # Initialize game state
    global current_state
    current_state = State(done_moves, available_moves)

    # Set click event
    figure.canvas.mpl_connect('button_press_event', lambda event: 
        on_click(event, choice))

    # Start turn
    current_state.next_turn()

    # Show window
    plt.show()


if __name__ == "__main__":
    main()