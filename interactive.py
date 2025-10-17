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
        'log_scale': True,  # Start with log scale for frequency response
        'dragging': None  # Track drag state: {'type': 'pole'/'zero', 'index': int, 'start_pos': complex}
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


    def on_press(event):
        """Handle mouse button press events."""
        # Check if click is inside pole-zero plot axes
        if event.inaxes != ax_pz:
            return

        # Get click location as complex number
        z_click = event.xdata + 1j * event.ydata

        # Left click: poles
        if event.button == 1:
            # Check if clicking near existing pole (for dragging)
            for i, pole in enumerate(state['poles']):
                if abs(pole - z_click) < CLICK_THRESHOLD:
                    # Start drag operation
                    state['dragging'] = {
                        'type': 'pole',
                        'index': i,
                        'start_pos': pole
                    }
                    return

            # If not near existing, add new pole
            state['poles'].append(z_click)
            redraw()

        # Right click: zeros
        elif event.button == 3:
            # Check if clicking near existing zero (for dragging)
            for i, zero in enumerate(state['zeros']):
                if abs(zero - z_click) < CLICK_THRESHOLD:
                    # Start drag operation
                    state['dragging'] = {
                        'type': 'zero',
                        'index': i,
                        'start_pos': zero
                    }
                    return

            # If not near existing, add new zero
            state['zeros'].append(z_click)
            redraw()


    def on_motion(event):
        """Handle mouse motion events for dragging."""
        # Only process if currently dragging
        if state['dragging'] is None:
            return

        # Check if still inside pole-zero plot axes
        if event.inaxes != ax_pz:
            return

        # Get new position as complex number
        z_new = event.xdata + 1j * event.ydata

        # Update position of dragged pole/zero
        drag_info = state['dragging']
        if drag_info['type'] == 'pole':
            state['poles'][drag_info['index']] = z_new
        else:  # zero
            state['zeros'][drag_info['index']] = z_new

        # Redraw for real-time visual feedback
        redraw()


    def on_release(event):
        """Handle mouse button release events."""
        # Only process if currently dragging
        if state['dragging'] is None:
            return

        drag_info = state['dragging']

        # Check if still inside pole-zero plot axes
        if event.inaxes == ax_pz:
            # Get final position
            z_final = event.xdata + 1j * event.ydata

            # Calculate distance moved from start
            distance_moved = abs(z_final - drag_info['start_pos'])

            # If barely moved, treat as click to remove
            if distance_moved < 0.05:
                if drag_info['type'] == 'pole':
                    state['poles'].pop(drag_info['index'])
                else:  # zero
                    state['zeros'].pop(drag_info['index'])
                redraw()
        else:
            # Released outside plot - revert to original position
            if drag_info['type'] == 'pole':
                state['poles'][drag_info['index']] = drag_info['start_pos']
            else:  # zero
                state['zeros'][drag_info['index']] = drag_info['start_pos']
            redraw()

        # Clear drag state
        state['dragging'] = None


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
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('key_press_event', onkey)

    # Initial draw
    redraw()

    # Print instructions
    print("\nInteractive Pole-Zero Plot Editor")
    print("=" * 50)
    print("Left click:   Add pole (red X)")
    print("Right click:  Add zero (blue O)")
    print("Drag:         Move existing pole/zero")
    print("Quick click:  Remove pole/zero (click without dragging)")
    print("Press 'l':    Toggle log/linear scale")
    print("Press 'c':    Clear all poles and zeros")
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
