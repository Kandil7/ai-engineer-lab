"""
11 - SciPy Image Processing
=============================
SciPy's ndimage module provides N-dimensional image processing
capabilities including filtering, interpolation, and measurements.

Topics:
- Image filtering (Gaussian, median, edge detection)
- Image morphology (erosion, dilation)
- Image measurements and labeling
- Image transformations (rotation, scaling)
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
from scipy import ndimage

# ============================================================
# Example 1: Basic Image Filtering
# ============================================================
print("=" * 60)
print("Example 1: Image Filtering with ndimage")
print("=" * 60)

# Create a synthetic image
np.random.seed(42)
size = 200
image = np.zeros((size, size))
# Add some shapes
image[40:80, 40:80] = 1.0  # White square
image[120:160, 120:160] = 0.7  # Gray square
image[60:140, 80:120] = 0.4  # Semi-transparent rectangle
# Add noise
image_noisy = image + np.random.normal(0, 0.15, (size, size))

# Gaussian smoothing
smoothed_3 = ndimage.gaussian_filter(image_noisy, sigma=3)
smoothed_7 = ndimage.gaussian_filter(image_noisy, sigma=7)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(image_noisy, cmap="gray", vmin=0, vmax=1.2)
axes[0].set_title("Noisy image")
axes[1].imshow(smoothed_3, cmap="gray", vmin=0, vmax=1.2)
axes[1].set_title("Gaussian sigma=3")
axes[2].imshow(smoothed_7, cmap="gray", vmin=0, vmax=1.2)
axes[2].set_title("Gaussian sigma=7")
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_smoothing.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_smoothing.png')}")

# Edge detection with Sobel filter
sx = ndimage.sobel(image, axis=0, mode="constant")
sy = ndimage.sobel(image, axis=1, mode="constant")
sob = np.hypot(sx, sy)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(sx, cmap="RdBu_r")
axes[1].set_title("Sobel X")
axes[2].imshow(sob, cmap="hot")
axes[2].set_title("Edge magnitude")
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_edges.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_edges.png')}")

# ============================================================
# Example 2: Morphological Operations
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Morphological Operations")
print("=" * 60)

# Create a binary image with noise
np.random.seed(42)
binary = np.zeros((150, 150), dtype=bool)
binary[30:70, 30:70] = True  # Square
binary[80:130, 80:130] = True  # Another square
# Add noise
noise = np.random.random((150, 150)) > 0.92
binary_noisy = binary | noise

# Morphological operations
struct = ndimage.generate_binary_structure(2, 1)  # 4-connectivity
eroded = ndimage.binary_erosion(binary_noisy, structure=struct, iterations=2)
dilated = ndimage.binary_dilation(binary_noisy, structure=struct, iterations=2)
opened = ndimage.binary_opening(binary_noisy, structure=struct, iterations=2)
closed = ndimage.binary_closing(binary_noisy, structure=struct, iterations=2)

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes[0, 0].imshow(binary, cmap="gray")
axes[0, 0].set_title("Original (clean)")
axes[0, 1].imshow(binary_noisy, cmap="gray")
axes[0, 1].set_title("With noise")
axes[0, 2].imshow(eroded, cmap="gray")
axes[0, 2].set_title("Erosion (2 iter)")
axes[1, 0].imshow(dilated, cmap="gray")
axes[1, 0].set_title("Dilation (2 iter)")
axes[1, 1].imshow(opened, cmap="gray")
axes[1, 1].set_title("Opening (noise removal)")
axes[1, 2].imshow(closed, cmap="gray")
axes[1, 2].set_title("Closing (gap filling)")
for ax in axes.flatten():
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_morphology.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_morphology.png')}")

# Count objects after cleaning
labeled_opened, n_opened = ndimage.label(opened)
print(f"Noisy image objects: {ndimage.label(binary_noisy)[1]}")
print(f"After opening:       {n_opened} objects")

# ============================================================
# Example 3: Image Measurement and Labeling
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Image Measurements and Labeling")
print("=" * 60)

# Create an image with distinct objects
np.random.seed(42)
img_labels = np.zeros((200, 200), dtype=bool)

# Object 1: circle
y, x = np.ogrid[:200, :200]
circle1 = (x - 50) ** 2 + (y - 50) ** 2 < 400
img_labels |= circle1

# Object 2: rectangle
img_labels[100:140, 30:90] = True

# Object 3: ellipse
ellipse = ((x - 150) ** 2 / 1500 + (y - 150) ** 2 / 500) < 1
img_labels |= ellipse

# Label connected components
labeled_array, num_features = ndimage.label(img_labels)
print(f"Number of connected objects: {num_features}")

# Measure properties of each object
for i in range(1, num_features + 1):
    object_mask = labeled_array == i
    # Centroid
    cy, cx = ndimage.center_of_mass(img_labels, labeled_array, i)
    # Area
    area = ndimage.sum(object_mask.astype(int), labeled_array, i)
    # Bounding box
    all_slices = ndimage.find_objects(labeled_array)
    s = all_slices[i - 1]
    bbox_h = s[0].stop - s[0].start
    bbox_w = s[1].stop - s[1].start
    # Intensity stats
    min_val = ndimage.minimum(img_labels.astype(float), labeled_array, i)
    max_val = ndimage.maximum(img_labels.astype(float), labeled_array, i)

    print(f"\n  Object {i}:")
    print(f"    Centroid: ({cx:.1f}, {cy:.1f})")
    print(f"    Area:     {area:.0f} pixels")
    print(f"    BBox:     {bbox_w}Ã—{bbox_h} pixels")

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(img_labels, cmap="gray")
axes[0].set_title("Original objects")
axes[1].imshow(labeled_array, cmap="nipy_spectral")
axes[1].set_title(f"Labeled ({num_features} objects)")
# Centroids overlay
for i in range(1, num_features + 1):
    cy, cx = ndimage.center_of_mass(img_labels, labeled_array, i)
    axes[1].plot(cx, cy, "k+", markersize=15, markeredgewidth=2)
axes[2].imshow(img_labels.astype(float) * labeled_array, cmap="hot")
axes[2].set_title("Weighted objects")
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_labeling.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_labeling.png')}")

# ============================================================
# Example 4: Image Transformations
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Image Transformations")
print("=" * 60)

# Create a test image
np.random.seed(42)
test_img = np.zeros((100, 100))
test_img[20:80, 20:80] = 1.0
test_img[35:65, 35:65] = 0.5

# Rotate
rotated_30 = ndimage.rotate(test_img, 30, reshape=False, mode="constant")
rotated_45 = ndimage.rotate(test_img, 45, reshape=True, mode="constant")

# Shift (translate)
shifted = ndimage.shift(test_img, [10, -15], mode="constant")

# Scale (zoom)
zoomed = ndimage.zoom(test_img, 1.5, mode="constant")

# Flip
flipped_h = np.flipud(test_img)  # Horizontal flip
flipped_v = np.fliplr(test_img)  # Vertical flip

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes[0, 0].imshow(test_img, cmap="gray")
axes[0, 0].set_title("Original")
axes[0, 1].imshow(rotated_30, cmap="gray")
axes[0, 1].set_title("Rotated 30Â°")
axes[0, 2].imshow(rotated_45, cmap="gray")
axes[0, 2].set_title("Rotated 45Â°")
axes[1, 0].imshow(shifted, cmap="gray")
axes[1, 0].set_title("Shifted [10, -15]")
axes[1, 1].imshow(zoomed, cmap="gray")
axes[1, 1].set_title(f"Zoomed 1.5Ã— ({zoomed.shape})")
axes[1, 2].imshow(flipped_h, cmap="gray")
axes[1, 2].set_title("Flipped vertically")
for ax in axes.flatten():
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_transforms.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_transforms.png')}")

print(f"\nOriginal shape: {test_img.shape}")
print(f"Rotated 45Â° shape: {rotated_45.shape}")
print(f"Zoomed shape: {zoomed.shape}")

# ============================================================
# Example 5: Histogram-based Analysis
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Image Histogram and Contrast Enhancement")
print("=" * 60)

# Create a low-contrast image
np.random.seed(42)
low_contrast = np.random.normal(loc=0.4, scale=0.1, size=(200, 200))
low_contrast = np.clip(low_contrast, 0, 1)

# Histogram equalization using scipy
from scipy.ndimage import uniform_filter1d

# Manual histogram equalization
hist, bins = np.histogram(low_contrast.ravel(), bins=256, range=(0, 1))
cdf = hist.cumsum()
cdf_normalized = cdf / cdf[-1]
# Map pixel values
equalized = np.interp(low_contrast.ravel(), bins[:-1], cdf_normalized).reshape(low_contrast.shape)

# CLAHE-like: contrast limited adaptive histogram equalization
# Simple version using local mean subtraction
local_mean = ndimage.uniform_filter(low_contrast, size=30)
adaptive_enhanced = np.clip((low_contrast - local_mean) * 2 + 0.5, 0, 1)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes[0, 0].imshow(low_contrast, cmap="gray", vmin=0, vmax=1)
axes[0, 0].set_title("Low contrast image")
axes[0, 1].imshow(equalized, cmap="gray", vmin=0, vmax=1)
axes[0, 1].set_title("Histogram equalized")
axes[1, 0].imshow(adaptive_enhanced, cmap="gray", vmin=0, vmax=1)
axes[1, 0].set_title("Adaptive enhancement")
# Histogram comparison
axes[1, 1].hist(low_contrast.ravel(), bins=50, alpha=0.5, label="Original", density=True)
axes[1, 1].hist(equalized.ravel(), bins=50, alpha=0.5, label="Equalized", density=True)
axes[1, 1].set_title("Histogram comparison")
axes[1, 1].legend()
for ax in axes.flatten():
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_11_contrast.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_11_contrast.png')}")

# Print statistics
print(f"\nImage statistics:")
print(f"  Original:      mean={low_contrast.mean():.4f}, std={low_contrast.std():.4f}")
print(f"  Equalized:     mean={equalized.mean():.4f}, std={equalized.std():.4f}")
print(f"  Adaptive:      mean={adaptive_enhanced.mean():.4f}, std={adaptive_enhanced.std():.4f}")

print("\n[OK] SciPy image processing covered!")
print("   Next: 12-io.py for file I/O operations.")
