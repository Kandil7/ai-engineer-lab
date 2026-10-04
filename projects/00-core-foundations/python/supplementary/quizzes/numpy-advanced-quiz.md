# NumPy Advanced Quiz

## Topic Overview
This quiz covers advanced NumPy concepts including advanced indexing, linear algebra, Fourier transforms, random distributions, memory management, and performance optimization. These topics are essential for scientific computing and data science applications.

**Difficulty:** Intermediate to Advanced
**Questions:** 20
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Medium]
**What is the difference between `arr[0:5]` and `arr.take([0,1,2,3,4])`?**

A) No difference
B) `take()` is always faster
C) `take()` works on flattened array, slicing preserves shape
D) Slicing creates a copy

**Correct Answer:** C
**Explanation:** Slicing preserves the original shape and creates a view. `take()` works on the flattened array by default and creates a copy. `take()` can be faster for fancy indexing operations.

---

### Question 2 [Hard]
**What is "fancy indexing" in NumPy?**

A) Indexing with boolean arrays
B) Indexing with integer arrays
C) Using `.fancy[]` method
D) Indexing with string labels

**Correct Answer:** B
**Explanation:** Fancy indexing uses integer arrays to select elements. You pass an array of indices, and NumPy returns an array of elements at those positions.

```python
arr = np.array([10, 20, 30, 40, 50])
indices = np.array([0, 2, 4])
arr[indices]  # [10, 30, 50]
```

---

### Question 3 [Hard]
**What does `np.einsum()` do?**

A) Eigenvalue decomposition
B) Einstein summation notation for array operations
C) Exponential sum
D) Element-wise sum

**Correct Answer:** B
**Explanation:** `np.einsum()` implements Einstein summation notation, allowing you to express complex array operations (dot products, outer products, transposes, traces) in a compact string notation.

```python
np.einsum("ij,jk->ik", A, B)  # Matrix multiplication
np.einsum("ii", A)  # Trace
np.einsum("ij->ji", A)  # Transpose
```

---

### Question 4 [Medium]
**How do you solve a system of linear equations `Ax = b`?**

A) `np.solve(A, b)`
B) `np.linalg.solve(A, b)`
C) `A.inverse() @ b`
D) Both A and B

**Correct Answer:** B
**Explanation:** `np.linalg.solve(A, b)` solves the system `Ax = b`. Note that `np.solve` is not a real function — calling it raises an `AttributeError`. Using the inverse (`A.inverse() @ b`) is numerically less stable and slower for large systems, and `A.inverse()` is not a valid NumPy method either.

---

### Question 5 [Hard]
**What is the purpose of `np strides`?**

A) To calculate the speed of operations
B) To define how many bytes to skip in memory for each dimension
C) To set iteration speed
D) To configure array alignment

**Correct Answer:** B
**Explanation:** Strides define how many bytes to move in memory for each index step in a dimension. Understanding strides helps optimize memory access patterns and explains why some views are faster than others.

---

### Question 6 [Medium]
**Which function computes the eigenvalues and eigenvectors of a matrix?**

A) `np.linalg.eig()`
B) `np.linalg.eigen()`
C) `np.eigvals()`
D) Both A and C

**Correct Answer:** D
**Explanation:** `np.linalg.eig()` returns both eigenvalues and eigenvectors. `np.linalg.eigvals()` returns only eigenvalues. Use `eigvals()` when you only need eigenvalues for better performance.

---

### Question 7 [Hard]
**What is the difference between `np.dot()` and `@` operator?**

A) No difference for 2D arrays
B) `@` is always faster
C) `np.dot()` supports higher dimensions
D) Both A and C

**Correct Answer:** D
**Explanation:** For 2D arrays, `np.dot(A, B)` and `A @ B` are equivalent. `@` is the matrix multiplication operator (PEP 465). `np.dot()` supports higher-dimensional arrays with specific broadcasting rules.

---

### Question 8 [Medium]
**How do you compute the singular value decomposition (SVD)?**

A) `np.linalg.svd()`
B) `np.svd()`
C) `np.linalg.singular()`
D) SVD is not available in NumPy

**Correct Answer:** A
**Explanation:** `np.linalg.svd()` returns the SVD of a matrix: U, S (singular values), and Vh. SVD is fundamental in dimensionality reduction, data compression, and solving least-squares problems.

---

### Question 9 [Hard]
**What is `np.memmap` used for?**

A) Memory mapping files for array storage
B) Creating memory-efficient arrays
C) Both A and B
D) Mapping memory addresses

**Correct Answer:** C
**Explanation:** `np.memmap` creates a NumPy array backed by a memory-mapped file. This allows working with arrays larger than RAM by loading only needed portions from disk.

---

### Question 10 [Medium]
**Which random distribution follows a bell curve?**

A) `np.random.uniform()`
B) `np.random.normal()`
C) `np.random.poisson()`
D) `np.random.binomial()`

**Correct Answer:** B
**Explanation:** `np.random.normal(loc, scale, size)` generates samples from a normal (Gaussian) distribution, which follows the classic bell curve. `loc` is mean, `scale` is standard deviation.

---

### Question 11 [Hard]
**What does `np.ufunc` represent?**

A) Universal functions for element-wise operations
B) User-defined functions
C) Utility functions
D) Union functions

**Correct Answer:** A
**Explanation:** Universal functions (ufuncs) are NumPy functions that perform element-wise operations on arrays. They are implemented in C for speed and support broadcasting, type casting, and output parameters.

---

### Question 12 [Medium]
**How do you compute the Fourier transform of an array?**

A) `np.fft.fft()`
B) `np.transform()`
C) `np.fourier()`
D) `np.fft.transform()`

**Correct Answer:** A
**Explanation:** `np.fft.fft()` computes the 1D Fast Fourier Transform. Related functions include `ifft()` (inverse), `fft2()` (2D), and `fftn()` (N-dimensional).

---

### Question 13 [Hard]
**What is the purpose of `np.lib.stride_tricks.as_strided()`?**

A) Creates views with custom strides
B) Changes array strides automatically
C) Optimizes stride calculations
D) Creates strided arrays

**Correct Answer:** A
**Explanation:** `as_strided()` creates a view of an array with custom strides. This is useful for implementing sliding window operations, im2col transformations, and other array manipulations without copying data.

---

### Question 14 [Medium]
**Which function computes the determinant of a matrix?**

A) `np.linalg.det()`
B) `np.linalg.determinant()`
C) `np.det()`
D) `np.matrix.det()`

**Correct Answer:** A
**Explanation:** `np.linalg.det()` computes the determinant of a square matrix. The determinant is used in matrix inversion, solving linear systems, and checking if a matrix is singular.

---

### Question 15 [Hard]
**What is "vectorization" in NumPy?**

A) Converting code to use vectors
B) Replacing explicit loops with array operations
C) Using SIMD instructions
D) Both B and C

**Correct Answer:** D
**Explanation:** Vectorization replaces Python loops with NumPy array operations, which are implemented in optimized C code. This leverages CPU SIMD instructions for massive performance gains.

---

### Question 16 [Medium]
**How do you compute the cross product of two vectors?**

A) `np.cross()`
B) `np.dot()`
C) `np.outer()`
D) `np.multiply()`

**Correct Answer:** A
**Explanation:** `np.cross(a, b)` computes the cross product of two vectors. The cross product is perpendicular to both input vectors and is used in physics, 3D graphics, and geometry.

---

### Question 17 [Hard]
**What is the purpose of `np.fromfunction()`?**

A) Creates arrays by evaluating a function at each coordinate
B) Imports functions from other modules
C) Converts functions to arrays
D) Creates function objects

**Correct Answer:** A
**Explanation:** `np.fromfunction()` creates an array where each element is computed by calling a function with the coordinates. Useful for creating arrays with specific patterns.

```python
np.fromfunction(lambda i, j: i + j, (3, 3))
# [[0, 1, 2],
#  [1, 2, 3],
#  [2, 3, 4]]
```

---

### Question 18 [Hard]
**What happens when you do `arr.flags.writeable = False`?**

A) The array becomes immutable
B) Raises an error if you try to modify
C) Both A and B
D) Only prevents deletion

**Correct Answer:** C
**Explanation:** Setting `writeable=False` makes the array read-only. Any attempt to modify it raises a `ValueError`. This is useful for ensuring data integrity and enabling certain optimizations.

---

### Question 19 [Medium]
**How do you stack arrays vertically?**

A) `np.vstack()`
B) `np.concatenate()` with axis=0
C) `np.r_[]`
D) All of the above

**Correct Answer:** D
**Explanation:** All three methods stack arrays vertically. `vstack()` and `np.r_[]` are syntactic sugar for `concatenate` with `axis=0`.

---

### Question 20 [Hard]
**What is `np.tensordot()` used for?**

A) Dot product along specified axes
B) Tensor multiplication
C) Both A and B
D) Computing tensor norms

**Correct Answer:** C
**Explanation:** `np.tensordot(a, b, axes)` computes the dot product along specified axes. It generalizes matrix multiplication to higher-dimensional arrays and is flexible for tensor operations.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | C |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | D |
| 7 | D |
| 8 | A |
| 9 | C |
| 10 | B |
| 11 | A |
| 12 | A |
| 13 | A |
| 14 | A |
| 15 | D |
| 16 | A |
| 17 | A |
| 18 | C |
| 19 | D |
| 20 | C |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered advanced NumPy! |
| 14-17 | Proficient - Strong understanding, ready for scientific computing |
| 10-13 | Developing - Good foundation, practice advanced patterns |
| 6-9 | Beginner - Review NumPy basics first |
| 0-5 | Novice - Start with NumPy basics quiz |

---

*Quiz created for AI Engineer Lab - Python Foundations*
