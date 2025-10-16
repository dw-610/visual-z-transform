"""
This script plots a pole-zero plot.
"""

# -----------------------------------------------------------------------------
# imports

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------


def plot_unit_circle(ax):
    """Plots the unit circle on an existing figure."""
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, color='black', linewidth=0.75)


def set_axis_limits(ax, poles: np.ndarray, zeros: np.ndarray):
    """Dynamically sets the axis limits of the plot."""
    poles_x = np.real(poles)
    poles_y = np.imag(poles)
    zeros_x = np.real(zeros)
    zeros_y = np.imag(zeros)
    max_x = max(max(np.abs(poles_x)), max(np.abs(zeros_x)))
    max_y = max(max(np.abs(poles_y)), max(np.abs(zeros_y)))
    lim = max(1.5, max_x + 0.5, max_y + 0.5)
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])


def plot_poles(ax, poles: np.ndarray):
    """Plots the poles on the pole-zero plot."""
    x = np.real(poles)
    y = np.imag(poles)
    ax.scatter(x, y, marker='x', color='red', s=100)


def plot_zeros(ax, zeros: np.ndarray):
    """Plots the zeros on the pole-zero plot."""
    x = np.real(zeros)
    y = np.imag(zeros)
    ax.scatter(x, y, marker='o', facecolors='none', edgecolors='blue', s=100)


def clean_up_plot(ax):
    """Cleans up the plot a bit."""
    ax.set_aspect('equal')  # makes unit circle actually circular
    ax.grid(True, alpha=0.3)  # grid for readability
    ax.axhline(y=0, color='k', linewidth=0.5)  # x-axis line through origin
    ax.axvline(x=0, color='k', linewidth=0.5)  # y-axis line through origin
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Pole-Zero Plot')


def pole_zero_plot(poles: np.ndarray, zeros: np.ndarray):

    _, ax = plt.subplots()

    plot_unit_circle(ax)
    plot_poles(ax, poles)
    plot_zeros(ax, zeros)
    set_axis_limits(ax, poles, zeros)
    clean_up_plot(ax)

    plt.show()


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    
    POLES = [0.5+0.5j, -1]
    ZEROS = [1j, -1j]

    pole_zero_plot(POLES, ZEROS)


# -----------------------------------------------------------------------------