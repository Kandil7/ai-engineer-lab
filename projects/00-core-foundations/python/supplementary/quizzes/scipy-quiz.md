# SciPy Quiz

## Topic Overview
SciPy is a scientific computing library built on NumPy, providing algorithms for optimization, integration, interpolation, eigenvalue problems, and other scientific computations. This quiz covers SciPy's core modules and their applications.

**Difficulty:** Intermediate to Advanced
**Questions:** 20
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What is SciPy primarily used for?**

A) Web development
B) Scientific and technical computing
C) Data visualization
D) Machine learning

**Correct Answer:** B
**Explanation:** SciPy provides modules for optimization, integration, interpolation, linear algebra, statistics, and other scientific computing tasks. It builds on NumPy's array operations.

---

### Question 2 [Easy]
**How do you import SciPy?**

A) `import scipy`
B) `from scipy import module`
C) Both A and B
D) `import sp`

**Correct Answer:** C
**Explanation:** You can import the whole library with `import scipy` or specific modules with `from scipy import optimize`. The latter is more common for specific tasks.

---

### Question 3 [Medium]
**Which SciPy module handles optimization?**

A) `scipy.optimize`
B) `scipy.minimize`
C) `scipy.optimization`
D) `scipy.solver`

**Correct Answer:** A
**Explanation:** `scipy.optimize` provides functions for minimization, root finding, curve fitting, and other optimization tasks. Key functions include `minimize()`, `root()`, and `curve_fit()`.

---

### Question 4 [Medium]
**What does `scipy.integrate.quad()` do?**

A) Integrates a function numerically
B) Creates quadratic equations
C) Computes quadrants
D) Creates quadratic surfaces

**Correct Answer:** A
**Explanation:** `quad()` computes a definite integral using adaptive quadrature. It returns the integral value and an estimate of the absolute error.

```python
from scipy import integrate
import numpy as np

result, error = integrate.quad(lambda x: x**2, 0, 1)
# result ≈ 0.3333...
```

---

### Question 5 [Hard]
**What is `scipy.interpolate` used for?**

A) Interpolating missing data
B) Constructing new data points between known data points
C) Both A and B
D) Only for 1D data

**Correct Answer:** C
**Explanation:** `scipy.interpolate` provides functions for interpolation (estimating values between known points) and can handle 1D, 2D, and higher-dimensional data.

---

### Question 6 [Medium]
**Which function finds the minimum of a function?**

A) `scipy.optimize.minimize()`
B) `scipy.optimize.min()`
C) `scipy.optimize.findmin()`
D) `scipy.optimize.minimum()`

**Correct Answer:** A
**Explanation:** `minimize()` finds the local minimum of a function. It supports multiple methods (BFGS, Nelder-Mead, L-BFGS-B, etc.) and constraints.

---

### Question 7 [Easy]
**What does `scipy.linalg` provide?**

A) Linear algebra functions
B) Statistical functions
C) Integration functions
D) Optimization functions

**Correct Answer:** A
**Explanation:** `scipy.linalg` provides advanced linear algebra operations beyond NumPy, including matrix decompositions (LU, QR, SVD), determinants, inverses, and solving linear systems.

---

### Question 8 [Medium]
**What does `scipy.stats.norm.pdf()` compute?**

A) Cumulative distribution function
B) Probability density function
C) Percentile function
D) Probability mass function

**Correct Answer:** B
**Explanation:** `pdf()` computes the probability density function. `cdf()` computes the cumulative distribution function, `ppf()` computes percentiles, and `pmf()` is for discrete distributions.

---

### Question 9 [Hard]
**What is `scipy.signal` used for?**

A) Signal processing (filtering, FFT, etc.)
B) Network signals
C) Traffic signals
D) Audio only

**Correct Answer:** A
**Explanation:** `scipy.signal` provides tools for signal processing including filtering (Butterworth, Chebyshev), spectral analysis, window functions, and wavelet transforms.

---

### Question 10 [Medium]
**Which function solves a system of linear equations?**

A) `scipy.linalg.solve()`
B) `scipy.linalg.solve_linear()`
C) `scipy.linalg.linearsolve()`
D) `scipy.solve()`

**Correct Answer:** A
**Explanation:** `scipy.linalg.solve(A, b)` solves the linear system `Ax = b`. It's optimized and supports various matrix formats.

---

### Question 11 [Hard]
**What does `scipy.sparse` provide?**

A) Sparse matrix formats and operations
B) Sparse data storage
C) Both A and B
D) Only CSR matrices

**Correct Answer:** C
**Explanation:** `scipy.sparse` provides efficient storage and operations for sparse matrices (matrices with mostly zeros). Formats include CSR, CSC, COO, and BSR.

---

### Question 12 [Medium]
**What is `scipy.optimize.curve_fit()` used for?**

A) Fitting curves to data points
B) Drawing curves
C) Creating curve shapes
D) Optimizing curve parameters

**Correct Answer:** A
**Explanation:** `curve_fit()` performs nonlinear least-squares fitting of a function to data. It returns optimal parameters and the covariance matrix.

```python
from scipy.optimize import curve_fit


def model(x, a, b):
    return a * np.exp(b * x)


popt, pcov = curve_fit(model, xdata, ydata)
```

---

### Question 13 [Hard]
**What does `scipy.spatial.distance` compute?**

A) Distances between points
B) Spatial relationships
C) Both A and B
D) Only Euclidean distance

**Correct Answer:** C
**Explanation:** `scipy.spatial.distance` provides functions for computing distances (Euclidean, Manhattan, cosine, etc.) and spatial relationships between points.

---

### Question 14 [Medium]
**Which module handles image processing in SciPy?**

A) `scipy.ndimage`
B) `scipy.image`
C) `scipy.img`
D) `scipy.picture`

**Correct Answer:** A
**Explanation:** `scipy.ndimage` provides n-dimensional image processing functions including filtering, interpolation, measurements, and morphology for multidimensional arrays.

---

### Question 15 [Hard]
**What is `scipy.fft` used for?**

A) Fast Fourier Transform operations
B) File transfer
C) Function transformations
D) Fast testing

**Correct Answer:** A
**Explanation:** `scipy.fft` provides FFT implementations for signal processing, spectral analysis, and other frequency-domain operations. It's often faster than NumPy's FFT.

---

### Question 16 [Medium]
**What does `scipy.stats.ttest_ind()` do?**

A) Performs an independent samples t-test
B) Tests correlation
C) Tests normality
D) Computes t-distribution

**Correct Answer:** A
**Explanation:** `ttest_ind()` performs an independent two-sample t-test to determine if two populations have the same mean. Returns t-statistic and p-value.

---

### Question 17 [Hard]
**What does `scipy.cluster.hierarchy` provide?**

A) Hierarchical clustering algorithms
B) Cluster visualization
C) Both A and B
D) K-means clustering only

**Correct Answer:** C
**Explanation:** `hierarchy` provides hierarchical clustering (agglomerative) with functions for linkage computation, dendrogram plotting, and cluster formation.

---

### Question 18 [Medium]
**What does `scipy.constants` provide?**

A) Physical and mathematical constants
B) Configuration constants
C) Programming constants
D) Mathematical functions

**Correct Answer:** A
**Explanation:** `scipy.constants` provides physical constants (speed of light, Planck's constant, etc.), mathematical constants (pi, golden ratio), and unit conversions.

---

### Question 19 [Hard]
**What is `scipy.io` used for?**

A) Input/output operations for various file formats
B) Network I/O only
C) Database operations
D) Console I/O

**Correct Answer:** A
**Explanation:** `scipy.io` provides functions for reading and writing various file formats including MATLAB (.mat), NetCDF, WAV audio, and ARFF files.

---

### Question 20 [Medium]
**How do you compute the determinant of a matrix in SciPy?**

A) `scipy.linalg.det()`
B) `scipy.linalg.determinant()`
C) `scipy.det()`
D) `scipy.matrix.det()`

**Correct Answer:** A
**Explanation:** `scipy.linalg.det()` computes the determinant of a square matrix. It uses LU decomposition for efficiency and is generally faster than NumPy's implementation.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | C |
| 3 | A |
| 4 | A |
| 5 | C |
| 6 | A |
| 7 | A |
| 8 | B |
| 9 | A |
| 10 | A |
| 11 | C |
| 12 | A |
| 13 | C |
| 14 | A |
| 15 | A |
| 16 | A |
| 17 | C |
| 18 | A |
| 19 | A |
| 20 | A |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered SciPy! |
| 14-17 | Proficient - Strong scientific computing skills |
| 10-13 | Developing - Good foundation, explore more modules |
| 6-9 | Beginner - Review SciPy modules |
| 0-5 | Novice - Start with SciPy documentation |

---

*Quiz created for AI Engineer Lab - Python Foundations*
