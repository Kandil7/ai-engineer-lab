"""
12 - SciPy I/O Operations
===========================
SciPy provides I/O functions for reading and writing data in various
scientific formats including MATLAB, Matrix Market, Wavefront, and more.

Topics:
- Loading and saving MATLAB .mat files
- Reading/writing Matrix Market format
- File I/O with numpy integration
- Working with .wav files
- Serializing scientific data
"""

import numpy as np

# Ensure output directory exists (Tier 0 fix: Windows + CI)
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy"
)
os.makedirs(OUT_DIR, exist_ok=True)

import os
import tempfile

# ============================================================
# Example 1: MATLAB File Format (.mat)
# ============================================================
print("=" * 60)
print("Example 1: MATLAB .mat File I/O")
print("=" * 60)

from scipy.io import loadmat, savemat

# Create some data to save
data_dict = {
    "array_1d": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
    "array_2d": np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float),
    "complex_array": np.array([1 + 2j, 3 + 4j, 5 + 6j]),
    "text_string": "Hello from SciPy",
}

# Save to .mat file
tmp_dir = tempfile.mkdtemp()
mat_file = os.path.join(tmp_dir, "data.mat")
savemat(mat_file, data_dict)
print(f"Saved .mat file: {mat_file}")
print(f"File size: {os.path.getsize(mat_file)} bytes")

# Load from .mat file
loaded = loadmat(mat_file)
print(f"\nLoaded keys: {[k for k in loaded.keys() if not k.startswith('__')]}")
for key in ["array_1d", "array_2d", "complex_array"]:
    print(f"  {key}: shape={loaded[key].shape}, dtype={loaded[key].dtype}")

# Verify round-trip
assert np.allclose(data_dict["array_1d"], loaded["array_1d"].flatten())
assert np.allclose(data_dict["array_2d"], loaded["array_2d"])
print("\nRound-trip verification: [OK] All arrays match")

# Save with compression
mat_compressed = os.path.join(tmp_dir, "data_compressed.mat")
savemat(mat_compressed, data_dict, do_compression=True)
print(f"Compressed size: {os.path.getsize(mat_compressed)} bytes")
print(f"Uncompressed size: {os.path.getsize(mat_file)} bytes")

# ============================================================
# Example 2: Matrix Market Format
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Matrix Market Format (.mtx)")
print("=" * 60)

from scipy.io import mmread, mmwrite
from scipy import sparse

# Create a sparse matrix
n = 10
A_sparse = sparse.random(n, n, density=0.3, format="csr")
A_sparse.data = np.round(A_sparse.data * 10)  # Integer-ish values

# Save as Matrix Market format
mtx_file = os.path.join(tmp_dir, "matrix.mtx")
mmwrite(mtx_file, A_sparse)
print(f"Saved Matrix Market file: {mtx_file}")
print(f"Matrix shape: {A_sparse.shape}")
print(f"Non-zero elements: {A_sparse.nnz}")

# Read back
A_loaded = mmread(mtx_file).tocsr()
print(f"Loaded shape: {A_loaded.shape}")
print(f"Loaded nnz: {A_loaded.nnz}")

# Verify
assert np.allclose(A_sparse.toarray(), A_loaded.toarray())
print("Round-trip verification: [OK] Matrices match")

# Show the file format
with open(mtx_file, "r") as f:
    lines = f.readlines()
print(f"\nMatrix Market file header (first 5 lines):")
for line in lines[:5]:
    print(f"  {line.strip()}")

# ============================================================
# Example 3: Working with WAV Files
# ============================================================
print("\n" + "=" * 60)
print("Example 3: WAV File I/O")
print("=" * 60)

from scipy.io import wavfile

# Generate a test audio signal
fs = 44100  # Sample rate
duration = 2.0  # seconds
t = np.arange(0, duration, 1 / fs)

# Create a chord: C major (C4, E4, G4)
freqs = [261.63, 329.63, 392.00]  # C4, E4, G4
signal = np.zeros_like(t)
for freq in freqs:
    signal += np.sin(2 * np.pi * freq * t)

# Add envelope (fade in/out)
envelope = np.ones_like(t)
fade_samples = int(0.1 * fs)
envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
signal *= envelope * 0.3  # Normalize amplitude

# Convert to 16-bit integer
signal_int16 = (signal * 32767).astype(np.int16)

# Save WAV file
wav_file = os.path.join(tmp_dir, "chord.wav")
wavfile.write(wav_file, fs, signal_int16)
print(f"Created WAV file: {wav_file}")
print(f"  Sample rate: {fs} Hz")
print(f"  Duration: {duration} s")
print(f"  Samples: {len(signal_int16)}")
print(f"  File size: {os.path.getsize(wav_file)} bytes")

# Read back
fs_read, data_read = wavfile.read(wav_file)
print(f"\nRead back:")
print(f"  Sample rate: {fs_read} Hz")
print(f"  Data shape: {data_read.shape}")
print(f"  Data type: {data_read.dtype}")
print(f"  Max amplitude: {np.max(np.abs(data_read))}")

# Plot waveform
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(10, 5))
axes[0].plot(t[:2000], signal_int16[:2000], "b-", linewidth=0.5)
axes[0].set_title("Waveform (first 2000 samples)")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")
axes[0].grid(True, alpha=0.3)

# Spectrum
fft_audio = np.fft.fft(signal_int16)
freqs_audio = np.fft.fftfreq(len(signal_int16), 1 / fs)
pos = freqs_audio > 0
axes[1].plot(freqs_audio[pos], np.abs(fft_audio[pos]), "r-", linewidth=0.8)
axes[1].set_title("Frequency Spectrum")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("Magnitude")
axes[1].set_xlim(0, 1000)
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_12_wav.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_12_wav.png')}")

# ============================================================
# Example 4: NumPy Binary Format (.npy, .npz)
# ============================================================
print("\n" + "=" * 60)
print("Example 4: NumPy Binary Format (.npy / .npz)")
print("=" * 60)

# Save individual arrays
npy_file = os.path.join(tmp_dir, "array.npy")
big_array = np.random.randn(1000, 100)
np.save(npy_file, big_array)
print(f"Saved .npy file: {npy_file}")
print(f"  Array shape: {big_array.shape}")
print(f"  File size: {os.path.getsize(npy_file)} bytes")

# Load back
loaded_npy = np.load(npy_file)
assert np.allclose(big_array, loaded_npy)
print(f"  Round-trip: [OK]")

# Save multiple arrays in .npz (compressed archive)
npz_file = os.path.join(tmp_dir, "arrays.npz")
array_a = np.random.randn(100, 50)
array_b = np.random.randint(0, 10, (50, 30))
array_c = np.array([1.0, 2.0, 3.0])
np.savez_compressed(npz_file, a=array_a, b=array_b, c=array_c)
print(f"\nSaved .npz file: {npz_file}")
print(f"  File size: {os.path.getsize(npz_file)} bytes")

# Load and inspect
loaded_npz = np.load(npz_file)
print(f"  Keys: {list(loaded_npz.keys())}")
for key in loaded_npz:
    print(f"  {key}: shape={loaded_npz[key].shape}, dtype={loaded_npz[key].dtype}")

# Compare with uncompressed
npz_uncompressed = os.path.join(tmp_dir, "arrays_uncompressed.npz")
np.savez(npz_uncompressed, a=array_a, b=array_b, c=array_c)
print(f"\n  Compressed: {os.path.getsize(npz_file)} bytes")
print(f"  Uncompressed: {os.path.getsize(npz_uncompressed)} bytes")
ratio = (1 - os.path.getsize(npz_file) / os.path.getsize(npz_uncompressed)) * 100
print(f"  Compression ratio: {ratio:.1f}%")

# ============================================================
# Example 5: Text File I/O for Scientific Data
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Text and Structured Data I/O")
print("=" * 60)

# Save data as structured text (CSV-like)
data_to_save = np.column_stack(
    [
        np.linspace(0, 10, 50),
        np.sin(np.linspace(0, 10, 50)),
        np.cos(np.linspace(0, 10, 50)),
    ]
)

# Save as CSV
csv_file = os.path.join(tmp_dir, "data.csv")
np.savetxt(csv_file, data_to_save, delimiter=",", header="x,sin_x,cos_x", comments="")
print(f"Saved CSV: {csv_file}")

# Load CSV
data_csv = np.loadtxt(csv_file, delimiter=",", skiprows=1)
print(f"Loaded CSV shape: {data_csv.shape}")

# Save with formatting control
fmt_file = os.path.join(tmp_dir, "formatted.txt")
np.savetxt(
    fmt_file,
    data_to_save[:5],
    fmt=["%8.4f", "%12.8f", "%12.8f"],
    header="x        sin_x        cos_x",
    comments="# ",
)
print(f"\nFormatted output:")
with open(fmt_file, "r") as f:
    print(f.read())

# Load with different delimiters
tab_file = os.path.join(tmp_dir, "tab_data.txt")
np.savetxt(tab_file, data_to_save[:5], delimiter="\t", fmt="%.6f")
data_tab = np.loadtxt(tab_file)
print(f"Tab-delimited load: shape={data_tab.shape}")

# Summary
print("\n" + "=" * 60)
print("I/O Format Summary")
print("=" * 60)
formats = {
    ".mat": "MATLAB format (scipy.io.savemat/loadmat)",
    ".mtx": "Matrix Market (scipy.io.mmwrite/mmread)",
    ".wav": "Wave audio (scipy.io.wavfile)",
    ".npy": "NumPy binary (np.save/load)",
    ".npz": "NumPy archive (np.savez/load)",
    ".csv": "Text CSV (np.savetxt/loadtxt)",
}
for fmt, desc in formats.items():
    print(f"  {fmt:<8s}: {desc}")

print("\n[OK] SciPy I/O module covered!")
print("   All 12 SciPy tutorial modules complete! *")
