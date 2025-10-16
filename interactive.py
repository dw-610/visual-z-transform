"""
Interactive pole-zero plot editor.

Click to add/remove poles and zeros:
- Left click: add/remove pole (red x)
- Right click: add/remove zero (blue o)
- Click near existing marker to remove it
"""

# -----------------------------------------------------------------------------
# imports

import numpy as np
import matplotlib.pyplot as plt
from plotting import (
    plot_unit_circle,
    plot_poles,
    plot_zeros,
    set_axis_limits,
    clean_up_plot
)

# -----------------------------------------------------------------------------


def interactive_pole_zero_plot(initial_poles=None, initial_zeros=None):
    """
    Launch an interactive pole-zero plot editor.

    Args:
        initial_poles: Initial pole locations (complex numbers)
        initial_zeros: Initial zero locations (complex numbers)
    """
    # Initialize state
    if initial_poles is None:
        initial_poles = []
    if initial_zeros is None:
        initial_zeros = []

    state = {
        'poles': list(initial_poles),
        'zeros': list(initial_zeros)
    }

    # Removal threshold (distance in complex plane)
    CLICK_THRESHOLD = 0.1

    # Create figure
    fig, ax = plt.subplots()


    def redraw():
        """Redraw the entire plot with current poles and zeros."""
        ax.clear()

        plot_unit_circle(ax)

        if state['poles']:
            plot_poles(ax, np.array(state['poles']))
        if state['zeros']:
            plot_zeros(ax, np.array(state['zeros']))

        # Set axis limits (with defaults if no poles/zeros)
        if state['poles'] or state['zeros']:
            poles_arr = (
                np.array(state['poles']) if state['poles']
                else np.array([0])
            )
            zeros_arr = (
                np.array(state['zeros']) if state['zeros']
                else np.array([0])
            )
            set_axis_limits(ax, poles_arr, zeros_arr)
        else:
            ax.set_xlim([-1.5, 1.5])
            ax.set_ylim([-1.5, 1.5])

        clean_up_plot(ax)
        fig.canvas.draw()


    def onclick(event):
        """Handle mouse click events."""
        # Check if click is inside axes
        if event.inaxes != ax:
            return

        # Get click location as complex number
        z_click = event.xdata + 1j * event.ydata

        # Left click: poles
        if event.button == 1:
            # Check if clicking near existing pole
            removed = False
            for i, pole in enumerate(state['poles']):
                if abs(pole - z_click) < CLICK_THRESHOLD:
                    state['poles'].pop(i)
                    removed = True
                    break

            # If didn't remove, add new pole
            if not removed:
                state['poles'].append(z_click)

        # Right click: zeros
        elif event.button == 3:
            # Check if clicking near existing zero
            removed = False
            for i, zero in enumerate(state['zeros']):
                if abs(zero - z_click) < CLICK_THRESHOLD:
                    state['zeros'].pop(i)
                    removed = True
                    break

            # If didn't remove, add new zero
            if not removed:
                state['zeros'].append(z_click)

        # Redraw the plot
        redraw()


    # Connect event handler
    fig.canvas.mpl_connect('button_press_event', onclick)

    # Initial draw
    redraw()

    # Print instructions
    print("\nInteractive Pole-Zero Plot Editor")
    print("=" * 40)
    print("Left click:  Add/remove pole (red X)")
    print("Right click: Add/remove zero (blue O)")
    print("Close window to exit")
    print("=" * 40)

    plt.show()


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    # Start with some example poles and zeros
    initial_poles = [0.5 + 0.5j, -0.8]
    initial_zeros = [1j, -1j]

    interactive_pole_zero_plot(initial_poles, initial_zeros)


# -----------------------------------------------------------------------------
