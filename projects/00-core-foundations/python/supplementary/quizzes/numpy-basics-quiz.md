# NumPy Basics Quiz

## Topic Overview
NumPy is the fundamental package for scientific computing in Python. It provides support for large, multi-dimensional arrays and matrices, along with mathematical functions to operate on these arrays efficiently. This quiz covers array creation, indexing, basic operations, and core concepts.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What does NumPy stand for?**

A) Number Python
B) Numerical Python
C) Numeric Python
D) Number Processing

**Correct Answer:** B
**Explanation:** NumPy stands for "Numerical Python". It was created in 2005 by Travis Oliphant and has become the de facto standard for numerical computing in Python.

---

### Question 2 [Easy]
**Which function creates a NumPy array from a Python list?**

A) `np.array()`
B) `np.list()`
C) `np.create()`
D) `np.fromlist()`

**Correct Answer:** A
**Explanation:** `np.array()` is the primary function for creating NumPy arrays. It can convert Python lists, tuples, and other array-like objects into NumPy arrays.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
```

---

### Question 3 [Easy]
**How do you check the shape of a NumPy array?**

A) `arr.dimensions()`
B) `arr.shape`
C) `np.shape(arr)`
D) Both B and C

**Correct Answer:** D
**Explanation:** Both `arr.shape` (attribute) and `np.shape(arr)` (function) return the shape of an array as a tuple. For example, a 3x4 array returns `(3, 4)`.

---

### Question 4 [Easy]
**What is the data type of `np.array([1, 2, 3])` by default?**

A) `float64`
B) `int32`
C) `int64`
D) `object`

**Correct Answer:** C
**Explanation:** On most systems, NumPy defaults to `int64` for integer arrays. You can specify a different type with `dtype=np.int32` or similar.

---

### Question 5 [Medium]
**Which function creates an array of all zeros?**

A) `np.zeros()`
B) `np.empty()`
C) `np.null()`
D) `np.zeros_like()`

**Correct Answer:** A
**Explanation:** `np.zeros((rows, cols))` creates an array filled with zeros. You pass the shape as a tuple. There's also `np.zeros_like()` which creates a zeros array matching another array's shape.

---

### Question 6 [Medium]
**What is the difference between `np.arange()` and `np.linspace()`?**

A) No difference
B) `arange` uses step size, `linspace` uses number of points
C) `arange` uses number of points, `linspace` uses step size
D) `arange` only works with integers

**Correct Answer:** B
**Explanation:** `np.arange(start, stop, step)` generates values with a specified step size. `np.linspace(start, stop, num)` generates a specified number of evenly spaced points between start and stop.

```python
np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
np.linspace(0, 10, 5)  # [0, 2.5, 5, 7.5, 10]
```

---

### Question 7 [Easy]
**How do you access the element at row 1, column 2 of a 2D array `arr`?**

A) `arr[1][2]`
B) `arr[1, 2]`
C) Both A and B
D) `arr.get(1, 2)`

**Correct Answer:** C
**Explanation:** NumPy supports both `arr[1][2]` and `arr[1, 2]` syntax for element access. The comma-separated syntax is preferred as it's faster and more explicit.

---

### Question 8 [Medium]
**What does `arr.reshape(3, 4)` do?**

A) Changes the array in-place to 3 rows, 4 columns
B) Returns a new array view with shape (3, 4)
C) Transposes the array
D) Flattens the array

**Correct Answer:** B
**Explanation:** `reshape()` returns a view of the array with the new shape (if possible). The original array is unchanged. The total number of elements must remain the same.

---

### Question 9 [Easy]
**Which function creates an identity matrix?**

A) `np.eye()`
B) `np.identity()`
C) Both A and B
D) `np.matrix()`

**Correct Answer:** C
**Explanation:** Both `np.eye(n)` and `np.identity(n)` create an n×n identity matrix. `np.eye()` is more flexible as it can also create non-square matrices and offset diagonals.

---

### Question 10 [Medium]
**What happens when you add a 1D array to a 2D array?**

A) Error
B) Broadcasting occurs
C) Returns None
D) Only works with same shapes

**Correct Answer:** B
**Explanation:** NumPy broadcasts the smaller array across the larger one. A 1D array is broadcast along the rows of the 2D array, adding the 1D values to each row.

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([10, 20, 30])
result = a + b  # [[11, 22, 33], [14, 25, 36]]
```

---

### Question 11 [Easy]
**How do you find the maximum value in an array?**

A) `arr.max()`
B) `np.max(arr)`
C) Both A and B
D) `max(arr)`

**Correct Answer:** C
**Explanation:** Both `arr.max()` and `np.max(arr)` return the maximum value. `np.max()` is more explicit and works with axis parameter for multi-dimensional arrays.

---

### Question 12 [Medium]
**What does `np.where()` do?**

A) Finds the indices where a condition is True
B) Replaces values based on a condition
C) Both A and B depending on arguments
D) Filters the array

**Correct Answer:** C
**Explanation:** With one argument (condition), `np.where()` returns indices where True. With three arguments (condition, x, y), it returns elements from x where True, else from y.

```python
arr = np.array([1, 5, 3, 8, 2])
indices = np.where(arr > 4)  # [1, 3]
result = np.where(arr > 4, arr, 0)  # [0, 5, 0, 8, 0]
```

---

### Question 13 [Hard]
**What is the difference between `arr.copy()` and `arr.view()`?**

A) No difference
B) `copy()` creates a deep copy, `view()` creates a shallow copy
C) `copy()` is faster
D) `view()` creates a deep copy

**Correct Answer:** B
**Explanation:** `copy()` creates an independent copy (changes don't affect original). `view()` creates a new view of the same data (changes DO affect original). Use `view()` for performance when you don't need independence.

---

### Question 14 [Medium]
**How do you concatenate two arrays along axis 0?**

A) `np.concatenate((a, b), axis=0)`
B) `np.vstack((a, b))`
C) Both A and B
D) `np.merge(a, b)`

**Correct Answer:** C
**Explanation:** `np.concatenate()` is the general function for joining arrays. `np.vstack()` (vertical stack) is equivalent to `concatenate` with `axis=0` for 2D arrays.

---

### Question 15 [Easy]
**What is the purpose of `np.random.seed()`?**

A) Generates random numbers
B) Sets the random number generator seed for reproducibility
C) Creates a random array
D) Initializes the random module

**Correct Answer:** B
**Explanation:** `np.random.seed()` sets the seed for the random number generator, ensuring reproducible results. Same seed = same sequence of random numbers.

---

### Question 16 [Medium]
**Which function computes the dot product of two arrays?**

A) `np.dot()`
B) `np.product()`
C) `np.multiply()`
D) `np.cross()`

**Correct Answer:** A
**Explanation:** `np.dot()` computes the dot product (scalar product) of two arrays. For 1D arrays, it's the sum of element-wise products. For 2D arrays, it's matrix multiplication.

---

### Question 17 [Hard]
**What does broadcasting allow you to do?**

A) Add arrays of different shapes
B) Perform element-wise operations on arrays of different shapes without explicit loops
C) Only works with scalar values
D) Concatenate arrays of different sizes

**Correct Answer:** B
**Explanation:** Broadcasting automatically expands arrays to compatible shapes for element-wise operations. Rules: arrays must have compatible dimensions, or one dimension must be 1.

```python
a = np.array([[1], [2], [3]])  # Shape (3, 1)
b = np.array([10, 20, 30])  # Shape (3,)
# Broadcasting works, result shape (3, 3)
```

---

### Question 18 [Medium]
**How do you select elements from an array based on a condition?**

A) Boolean indexing: `arr[arr > 5]`
B) `np.select()`
C) `np.filter()`
D) `np.mask()`

**Correct Answer:** A
**Explanation:** Boolean indexing uses a boolean array to select elements. `arr[condition]` returns a 1D array of elements where the condition is True.

---

### Question 19 [Hard]
**What is the `axis` parameter in NumPy functions?**

A) The direction along which the operation is performed
B) The data type of the array
C) The number of dimensions
D) The array index

**Correct Answer:** A
**Explanation:** The `axis` parameter specifies the dimension along which to operate. `axis=0` operates along rows (down columns), `axis=1` operates along columns (across rows). Negative indices count from the end.

---

### Question 20 [Medium]
**Which function computes the mean of an array?**

A) `arr.mean()`
B) `np.mean(arr)`
C) Both A and B
D) `np.average()`

**Correct Answer:** C
**Explanation:** Both `arr.mean()` and `np.mean(arr)` compute the arithmetic mean. `np.average()` is similar but also supports weights. All accept `axis` parameter for multi-dimensional arrays.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | A |
| 3 | D |
| 4 | C |
| 5 | A |
| 6 | B |
| 7 | C |
| 8 | B |
| 9 | C |
| 10 | B |
| 11 | C |
| 12 | C |
| 13 | B |
| 14 | C |
| 15 | B |
| 16 | A |
| 17 | B |
| 18 | A |
| 19 | A |
| 20 | C |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered NumPy basics! |
| 14-17 | Proficient - Strong foundation, ready for advanced topics |
| 10-13 | Developing - Good start, practice more |
| 6-9 | Beginner - Review array fundamentals |
| 0-5 | Novice - Start with NumPy documentation |

---

*Quiz created for AI Engineer Lab - Python Foundations*
