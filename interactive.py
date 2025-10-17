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
    clean_up_plot,
    plot_frequency_response_on_axis
)
from frequency_response import get_frequency_response

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
        'zeros': list(initial_zeros),
        'log_scale': True  # Start with log scale for frequency response
    }

    # Removal threshold (distance in complex plane)
    CLICK_THRESHOLD = 0.1

    # Create figure with two subplots side by side
    fig, (ax_pz, ax_freq) = plt.subplots(1, 2, figsize=(14, 6))


    def redraw():
        """Redraw the entire plot with current poles and zeros."""
        # Clear both axes
        ax_pz.clear()
        ax_freq.clear()

        # Redraw pole-zero plot
        plot_unit_circle(ax_pz)

        if state['poles']:
            plot_poles(ax_pz, np.array(state['poles']))
        if state['zeros']:
            plot_zeros(ax_pz, np.array(state['zeros']))

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
            set_axis_limits(ax_pz, poles_arr, zeros_arr)
        else:
            ax_pz.set_xlim([-1.5, 1.5])
            ax_pz.set_ylim([-1.5, 1.5])

        clean_up_plot(ax_pz)

        # Compute and plot frequency response (only if poles or zeros exist)
        if state['poles'] or state['zeros']:
            w, H = get_frequency_response(state['poles'], state['zeros'])
            plot_frequency_response_on_axis(ax_freq, w, H, log=state['log_scale'])
            ax_freq.set_title('Frequency Response')
        else:
            # No poles or zeros - show empty plot with message
            ax_freq.text(0.5, 0.5, 'Add poles/zeros to see frequency response',
                        ha='center', va='center', transform=ax_freq.transAxes,
                        fontsize=12, alpha=0.5)
            ax_freq.set_title('Frequency Response')

        plt.tight_layout()
        fig.canvas.draw()


    def onclick(event):
        """Handle mouse click events."""
        # Check if click is inside pole-zero plot axes
        if event.inaxes != ax_pz:
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


    def onkey(event):
        """Handle keyboard events."""
        if event.key == 'l':
            # Toggle log scale
            state['log_scale'] = not state['log_scale']
            redraw()
        elif event.key == 'c':
            # Clear all poles and zeros
            state['poles'].clear()
            state['zeros'].clear()
            redraw()

    # Connect event handlers
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', onkey)

    # Initial draw
    redraw()

    # Print instructions
    print("\nInteractive Pole-Zero Plot Editor")
    print("=" * 50)
    print("Left click:  Add/remove pole (red X)")
    print("Right click: Add/remove zero (blue O)")
    print("Press 'l':   Toggle log/linear scale")
    print("Press 'c':   Clear all poles and zeros")
    print("Close window to exit")
    print("=" * 50)

    plt.show()


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    # Start with some example poles and zeros
    initial_poles = [0.5 + 0.5j, -0.8]
    initial_zeros = [1j, -1j]

    interactive_pole_zero_plot(initial_poles, initial_zeros)


# -----------------------------------------------------------------------------
