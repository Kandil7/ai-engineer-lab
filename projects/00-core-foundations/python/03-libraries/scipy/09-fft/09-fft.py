"""
09 - SciPy FFT (Fast Fourier Transform)
========================================
The FFT converts signals between time/spatial domain and frequency domain.
SciPy provides optimized FFT implementations.

Topics:
- 1D FFT and inverse FFT
- 2D FFT for images
- Frequency spectrum analysis
- Power spectral density
- Windowing functions
"""

import numpy as np

# Ensure output directory exists (Tier 0 fix: Windows + CI)
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy"
)
os.makedirs(OUT_DIR, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import fft as sp_fft

# ============================================================
# Example 1: Basic 1D FFT
# ============================================================
print("=" * 60)
print("Example 1: Basic 1D FFT and Inverse FFT")
print("=" * 60)

# Create a signal: sum of two sinusoids
np.random.seed(42)
fs = 500  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)

# Signal: 50 Hz + 120 Hz + noise
freq1, freq2 = 50, 120
signal = np.sin(2 * np.pi * freq1 * t) + 0.5 * np.sin(2 * np.pi * freq2 * t)
signal_noisy = signal + 0.3 * np.random.randn(len(t))

# Compute FFT
fft_vals = sp_fft.fft(signal_noisy)
freqs = sp_fft.fftfreq(len(t), 1 / fs)

# Keep only positive frequencies
pos_mask = freqs >= 0
freqs_pos = freqs[pos_mask]
magnitude = np.abs(fft_vals[pos_mask]) / len(t) * 2  # Normalized magnitude

# Find dominant frequencies
peak_indices = np.argsort(magnitude)[-5:][::-1]
print("Detected dominant frequencies:")
for idx in peak_indices:
    print(f"  {freqs_pos[idx]:.1f} Hz (magnitude: {magnitude[idx]:.4f})")

# Inverse FFT to reconstruct
reconstructed = sp_fft.ifft(fft_vals).real
reconstruction_error = np.max(np.abs(signal_noisy - reconstructed))
print(f"\nInverse FFT reconstruction error: {reconstruction_error:.2e}")

# Plot
fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(t[:100], signal_noisy[:100], "b-", linewidth=1, alpha=0.7, label="Noisy signal")
axes[0].plot(t[:100], signal[:100], "r--", linewidth=2, label="Clean signal")
axes[0].set_title(f"Time Domain: {freq1} Hz + {freq2} Hz + noise")
axes[0].set_xlabel("Time (s)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].stem(freqs_pos[:200], magnitude[:200], linefmt="b-", markerfmt="bo", basefmt="k-")
axes[1].axvline(x=freq1, color="r", linestyle="--", alpha=0.7, label=f"{freq1} Hz")
axes[1].axvline(x=freq2, color="g", linestyle="--", alpha=0.7, label=f"{freq2} Hz")
axes[1].set_title("Frequency Spectrum (FFT)")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("Magnitude")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_basic_fft.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_basic_fft.png')}")

# ============================================================
# Example 2: Power Spectral Density
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Power Spectral Density (PSD)")
print("=" * 60)

# Generate a signal with multiple components
np.random.seed(42)
fs = 1000
t = np.arange(0, 2, 1 / fs)

# Complex signal: chirp + sinusoid + noise
chirp_freq = np.linspace(10, 200, len(t))
chirp = np.sin(2 * np.pi * chirp_freq * t)
tone = 0.5 * np.sin(2 * np.pi * 50 * t)
noise = 0.2 * np.random.randn(len(t))
signal_psd = chirp + tone + noise

# Compute PSD using Welch's method (via scipy.signal)
# Use manual periodogram if welch not available
fft_result = sp_fft.fft(signal_psd)
freqs_full = sp_fft.fftfreq(len(t), 1 / fs)
psd = np.abs(fft_result) ** 2 / len(t)
pos_mask = freqs_full > 0

# Also compute using scipy.signal if available
try:
    from scipy.signal import welch as scipy_welch

    f_welch, psd_welch = scipy_welch(signal_psd, fs=fs, nperseg=512)
    use_welch = True
except ImportError:
    use_welch = False

fig, ax = plt.subplots(figsize=(10, 4))
if use_welch:
    ax.semilogy(f_welch, psd_welch, "b-", linewidth=1.5, label="Welch PSD")
else:
    ax.semilogy(freqs_full[pos_mask], psd[pos_mask], "b-", linewidth=1.5, label="Periodogram")
ax.set_title("Power Spectral Density")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Power/Frequency (dB/Hz)")
ax.axvline(x=50, color="r", linestyle="--", alpha=0.7, label="50 Hz tone")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_psd.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_psd.png')}")

print(f"Signal length: {len(t)} samples")
print(f"Sampling rate: {fs} Hz")
print(f"Frequency resolution: {fs / len(t):.2f} Hz")

# ============================================================
# Example 3: 2D FFT (Image Processing)
# ============================================================
print("\n" + "=" * 60)
print("Example 3: 2D FFT for Image Analysis")
print("=" * 60)

# Create a synthetic image with patterns
np.random.seed(42)
size = 256
x = np.arange(size)
X, Y = np.meshgrid(x, x)

# Image with horizontal and diagonal lines
image = (
    np.sin(2 * np.pi * 20 * Y / size)
    + 0.5 * np.sin(2 * np.pi * 15 * (X + Y) / size)
    + 0.3 * np.random.randn(size, size)
)

# 2D FFT
fft_2d = sp_fft.fft2(image)
fft_shifted = sp_fft.fftshift(fft_2d)  # Center zero frequency
magnitude_2d = np.log1p(np.abs(fft_shifted))  # Log scale for visualization

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original Image")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")

axes[1].imshow(magnitude_2d, cmap="viridis")
axes[1].set_title("2D FFT Magnitude (log scale)")
axes[1].set_xlabel("u (frequency)")
axes[1].set_ylabel("v (frequency)")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_2d_fft.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_2d_fft.png')}")

# Low-pass filtering in frequency domain
rows, cols = image.shape
crow, ccol = rows // 2, cols // 2
cutoff = 30  # Low-pass cutoff frequency

# Create low-pass filter mask
mask = np.zeros((rows, cols))
Y_grid, X_grid = np.ogrid[:rows, :cols]
mask_area = (X_grid - ccol) ** 2 + (Y_grid - crow) ** 2 <= cutoff**2
mask[mask_area] = 1

# Apply filter and inverse FFT
filtered_fft = fft_shifted * mask
filtered_image = sp_fft.ifft2(sp_fft.ifftshift(filtered_fft)).real

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(mask, cmap="gray")
axes[1].set_title(f"Low-pass filter (cutoff={cutoff})")
axes[2].imshow(filtered_image, cmap="gray")
axes[2].set_title("Filtered image")
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_lowpass.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_lowpass.png')}")

# ============================================================
# Example 4: Windowing Functions
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Windowing Functions for FFT")
print("=" * 60)

from scipy.signal import windows

# Compare different window functions
window_names = ["hann", "hamming", "blackman", "kaiser"]
N = 256

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for ax, name in zip(axes, window_names):
    window_func = getattr(windows, name)
    if name == "kaiser":
        w = window_func(N, beta=14)
    else:
        w = window_func(N)
    ax.plot(w, "b-", linewidth=2)
    ax.set_title(f"{name.capitalize()} Window (N={N})")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.1, 1.1)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_windows.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_windows.png')}")

# Effect of windowing on spectral leakage
np.random.seed(42)
fs = 1000
t = np.arange(0, 1, 1 / fs)
freq = 50.5  # Not an integer number of cycles -> leakage
signal_win = np.sin(2 * np.pi * freq * t)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# No window
fft_no_win = sp_fft.fft(signal_win)
freqs_win = sp_fft.fftfreq(len(t), 1 / fs)
axes[0].plot(freqs_win[: len(t) // 2], np.abs(fft_no_win[: len(t) // 2]), "b-")
axes[0].set_title("No window (spectral leakage)")
axes[0].set_xlabel("Frequency (Hz)")
axes[0].set_xlim(0, 100)
axes[0].grid(True, alpha=0.3)

# With Blackman window
w = windows.blackman(len(signal_win))
fft_win = sp_fft.fft(signal_win * w)
axes[1].plot(freqs_win[: len(t) // 2], np.abs(fft_win[: len(t) // 2]), "r-")
axes[1].set_title("Blackman window (reduced leakage)")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_xlim(0, 100)
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_window_effect.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_window_effect.png')}")

# ============================================================
# Example 5: FFT-based Convolution
# ============================================================
print("\n" + "=" * 60)
print("Example 5: FFT-based Fast Convolution")
print("=" * 60)

from scipy.signal import fftconvolve

# Create two signals
np.random.seed(42)
signal_a = np.random.randn(1000)
signal_b = np.random.randn(100)

# Time-domain convolution vs FFT-based
import time

# Direct convolution
start = time.time()
result_direct = np.convolve(signal_a, signal_b, mode="full")
time_direct = time.time() - start

# FFT-based convolution
start = time.time()
result_fft = fftconvolve(signal_a, signal_b, mode="full")
time_fft = time.time() - start

# Compare results
max_error = np.max(np.abs(result_direct - result_fft))
print(f"Signal A length: {len(signal_a)}")
print(f"Signal B length: {len(signal_b)}")
print(f"Result length:   {len(result_direct)}")
print(f"Max difference:  {max_error:.2e}")
print(f"np.convolve time: {time_direct * 1000:.3f} ms")
print(f"fftconvolve time: {time_fft * 1000:.3f} ms")
print(f"Speedup: {time_direct / max(time_fft, 1e-10):.1f}x")

# Plot input signals and convolution result
fig, axes = plt.subplots(3, 1, figsize=(10, 8))
axes[0].plot(signal_a[:200], "b-", linewidth=0.8)
axes[0].set_title("Signal A (first 200 samples)")
axes[0].grid(True, alpha=0.3)

axes[1].plot(signal_b, "r-", linewidth=1.5)
axes[1].set_title("Signal B (impulse response)")
axes[1].grid(True, alpha=0.3)

axes[2].plot(result_fft, "g-", linewidth=0.8)
axes[2].set_title(f"Convolution result (length={len(result_fft)})")
axes[2].set_xlabel("Sample")
axes[2].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_09_convolution.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_09_convolution.png')}")

print("\n[OK] SciPy FFT module covered!")
print("   Next: 10-spatial-data.py for spatial computations.")
