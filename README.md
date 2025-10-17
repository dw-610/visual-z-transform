# Visual Z-Transform

An interactive tool for visualizing digital filter pole-zero plots and their corresponding frequency responses in real-time.

## Features

- **Interactive Pole-Zero Placement**: Click to add/remove poles and zeros on the complex z-plane
- **Real-time Frequency Response**: Automatically updates magnitude response as you modify poles/zeros
- **Dual Plot Display**: Side-by-side pole-zero and frequency response visualization
- **Log/Linear Scale Toggle**: Switch between dB and linear magnitude scales

## Installation

1. Clone the repository or download the files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Tool

Run the interactive pole-zero editor:

```bash
python interactive.py
```

**Controls:**
- **Left click**: Add/remove pole (red X)
- **Right click**: Add/remove zero (blue O)
- **Press 'l'**: Toggle log/linear scale on frequency response
- **Press 'c'**: Clear all poles and zeros
- **Close window**: Exit

Click near an existing pole or zero to remove it. The frequency response updates automatically.

### Standalone Frequency Response

Compute and plot frequency response from pole/zero lists:

```bash
python frequency_response.py
```

Edit the `POLES` and `ZEROS` lists in the file to analyze different filter configurations. Several example filters are included as comments.

### Pole-Zero Plotting Only

Generate static pole-zero plots:

```bash
python plotting.py
```

## How It Works

### Z-Transform Theory

The z-transform represents discrete-time signals and systems in the complex frequency domain. For a system with poles $p_i$ and zeros $z_i$, the transfer function is:

$$H(z) = \frac{\prod_i (1 - z_i z^{-1})}{\prod_j (1 - p_j z^{-1})}$$

The frequency response is obtained by evaluating $H(z)$ on the unit circle where $z = e^{j\omega}$:

$$H(e^{j\omega}) = \frac{\prod_i (1 - z_i e^{-j\omega})}{\prod_j (1 - p_j e^{-j\omega})}$$

### Implementation

- **Pole-Zero Plot**: Shows pole and zero locations in the complex z-plane with the unit circle for stability reference
- **Frequency Response**: Magnitude $|H(e^{j\omega})|$ plotted vs. frequency $\omega$ from $-\pi$ to $\pi$ rad/sample
- **Log Scale**: Displays magnitude in dB: $20 \log_{10}|H(e^{j\omega})|$

## Requirements

- Python 3.7+
- NumPy >= 1.24.0
- Matplotlib >= 3.7.0
