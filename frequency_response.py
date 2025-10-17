"""
Given poles/zeros, computes/plots the frequency response from the z transform.
"""

# -----------------------------------------------------------------------------
# imports

import numpy as np
from plotting import plot_frequency_response

# -----------------------------------------------------------------------------


def get_frequency_response(poles: list, zeros: list):
    """Given poles and zeros, computes the frequency response H(e^jω)."""
    
    w = np.linspace(-np.pi, np.pi, 1000)
    z = np.exp(1j * w)

    convert = lambda pz: (1 - pz*(1/z))

    num_terms = [convert(zero) for zero in zeros]
    dnm_terms = [convert(pole) for pole in poles]

    numerator = np.prod(num_terms, axis=0) if num_terms else 1.0
    denominator = np.prod(dnm_terms, axis=0) if dnm_terms else 1.0

    H = numerator / denominator

    return w, H


# -----------------------------------------------------------------------------


if __name__ == "__main__":

    # Example 1: Notch filter at π/2 (zeros on unit circle at +-j)
    # POLES = []
    # ZEROS = [1j, -1j]

    # Example 2: Resonant peak at π/2 (poles near unit circle at +-)
    # POLES = [0.9j, -0.9j]
    # ZEROS = []

    # Example 3: Low-pass filter (zero at z=-1, pole inside)
    # POLES = [0.8]
    # ZEROS = [-1]

    # Example 4: Band-pass filter
    # POLES = [0.9*np.exp(1j*np.pi/4), 0.9*np.exp(-1j*np.pi/4)]
    # ZEROS = [1, -1]

    # Example 5: Complex filter with multiple poles and zeros
    POLES = [0.8*np.exp(1j*np.pi/3), 0.8*np.exp(-1j*np.pi/3)]
    ZEROS = [1, -1, 1j, -1j]

    w, H = get_frequency_response(POLES, ZEROS)

    plot_frequency_response(w, H, log=True)


# -----------------------------------------------------------------------------