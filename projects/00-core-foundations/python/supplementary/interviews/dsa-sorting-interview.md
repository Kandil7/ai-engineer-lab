# DSA Sorting Interview Practice

## Topic Overview

Sorting is a fundamental algorithmic skill. Interviews test your knowledge of **time/space complexity**, **stability**, **when to use which algorithm**, and **sorting-based problem solving**. Understanding the trade-offs between algorithms is more important than memorizing code.

**Key Concepts:**
- **In-place:** Uses O(1) extra space
- **Stable:** Equal elements maintain relative order
- **Adaptive:** Faster on partially sorted input
- **Online:** Can sort elements as they arrive

---

## Interview Questions (with Answers)

### Q1: Compare all major sorting algorithms.

**Answer:**

| Algorithm | Best | Average | Worst | Space | Stable | In-place |
|-----------|------|---------|-------|-------|--------|----------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | No |
| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes | No |
| Bucket Sort | O(n + k) | O(n + k) | O(n²) | O(n) | Yes | No |

Where n = number of elements, k = range of input, d = number of digits.

---

### Q2: Explain Quick Sort. Why is it O(n²) worst case?

**Answer:**
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
```

**Worst case O(n²):** When the pivot is always the smallest or largest element (already sorted array with first/last element as pivot).

**Solutions:**
- Random pivot selection
- Median-of-three pivot
- Introsort (switch to heapsort when depth > log n)

**In-place version:**
```python
def quick_sort_inplace(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

### Q3: Explain Merge Sort. Why is it preferred over Quick Sort?

**Answer:**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Advantages over Quick Sort:**
1. **Guaranteed O(n log n):** No worst-case degradation
2. **Stable:** Maintains relative order of equal elements
3. **Better for linked lists:** No random access needed

**Disadvantage:** O(n) extra space (Quick Sort is in-place).

---

### Q4: When would you use Insertion Sort?

**Answer:**
Insertion Sort is optimal for:
1. **Small arrays (n < 20):** Low overhead beats O(n log n) algorithms
2. **Nearly sorted arrays:** O(n) best case, adaptive
3. **Online sorting:** Elements arrive one at a time
4. **As a subroutine:** Timsort uses insertion sort for small runs

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

**Why it's good for small n:** No recursion overhead, cache-friendly, adaptive.

---

### Q5: What is Heap Sort? How does it work?

**Answer:**
Heap Sort uses a binary heap data structure.

```python
def heap_sort(arr):
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

**Time: O(n log n), Space: O(1)**
**Use when:** Need guaranteed O(n log n) and O(1) space.

---

### Q6: What is Timsort? Why does Python use it?

**Answer:**
Timsort is a hybrid of Merge Sort and Insertion Sort. It's Python's default sorting algorithm.

**Key properties:**
- O(n log n) worst case
- O(n) best case (already sorted)
- Stable
- Adaptive (fast on partially sorted data)
- Uses insertion sort for small runs (≤64 elements)
- Merges runs efficiently

**Python's sorted() and list.sort() use Timsort.** It's optimized for real-world data that often has existing order.

---

### Q7: Explain Counting Sort. When can you use it?

**Answer:**
Counting Sort counts occurrences of each element. Only works for non-negative integers with a known range.

```python
def counting_sort(arr, k):
    count = [0] * k
    for num in arr:
        count[num] += 1

    result = []
    for i in range(k):
        result.extend([i] * count[i])

    return result


# With negative numbers
def counting_sort_negatives(arr):
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1

    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1

    result = []
    for i in range(range_val):
        result.extend([i + min_val] * count[i])

    return result
```

**When to use:** Small range of integers (k << n). Not suitable for floating-point numbers or large ranges.

---

### Q8: What is Radix Sort? How does it differ from Counting Sort?

**Answer:**
Radix Sort sorts digit by digit, from least significant to most significant (LSD) or vice versa (MSD).

```python
def radix_sort(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10


def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    arr[:] = output
```

**Time: O(d * (n + k))** where d = number of digits, k = base (10 for decimal)

**Difference from Counting Sort:**
- Radix Sort uses Counting Sort as a subroutine
- Radix Sort handles larger ranges by sorting digit by digit
- Counting Sort is better when range k is small

---

### Q9: When should you use which sorting algorithm?

**Answer:**

| Scenario | Algorithm | Reason |
|----------|-----------|--------|
| Small array (n < 20) | Insertion Sort | Low overhead, simple |
| Nearly sorted | Insertion Sort / Timsort | O(n) adaptive |
| General purpose | Timsort (Python's sorted) | Best of both worlds |
| Guaranteed O(n log n) | Merge Sort / Heap Sort | No worst case |
| Memory constrained | Heap Sort / Quick Sort | O(1) / O(log n) space |
| Stability required | Merge Sort / Timsort | Stable sorts |
| Integers with small range | Counting Sort | O(n + k) |
| Large integers / strings | Radix Sort | O(d * n) |
| Linked list | Merge Sort | No random access needed |
| External sorting (disk) | Merge Sort | Sequential access |

---

### Q10: How do you sort a linked list?

**Answer:**
Merge Sort is ideal for linked lists (no random access needed, stable).

```python
def sort_list(head):
    if not head or not head.next:
        return head

    # Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    left = sort_list(head)
    right = sort_list(mid)

    return merge(left, right)


def merge(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

---

### Q11: How do you find the kth largest element in an unsorted array?

**Answer:**
**Approach 1 — Sort (O(n log n)):**
```python
def find_kth_largest_sort(nums, k):
    return sorted(nums)[-k]
```

**Approach 2 — Min Heap (O(n log k)):**
```python
import heapq


def find_kth_largest_heap(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]
```

**Approach 3 — Quickselect (O(n) average):**
```python
import random


def find_kth_largest_quickselect(nums, k):
    target = len(nums) - k

    def quickselect(left, right):
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            return quickselect(store + 1, right)
        else:
            return quickselect(left, store - 1)

    return quickselect(0, len(nums) - 1)
```

---

### Q12: How do you sort colors (Dutch National Flag)?

**Answer:**
```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


# Test
nums = [2, 0, 2, 1, 1, 0]
sort_colors(nums)
assert nums == [0, 0, 1, 1, 2, 2]
```

**Time: O(n), Space: O(1)** — Single pass, three-way partition.

---

### Q13: How do you merge two sorted arrays?

**Answer:**
```python
def merge_sorted_arrays(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1

    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


# Test
nums1 = [1, 2, 3, 0, 0, 0]
merge_sorted_arrays(nums1, 3, [2, 5, 6], 3)
assert nums1 == [1, 2, 2, 3, 5, 6]
```

---

### Q14: What is the difference between stable and unstable sorting?

**Answer:**
**Stable sort:** Equal elements maintain their relative order from the input.

**Example:**
Input: [(A, 1), (B, 2), (C, 1)]
Stable sort by value: [(A, 1), (C, 1), (B, 2)] — A before C
Unstable sort by value: [(C, 1), (A, 1), (B, 2)] — C before A

**Stable algorithms:** Insertion Sort, Merge Sort, Bubble Sort, Timsort, Counting Sort, Radix Sort

**Unstable algorithms:** Quick Sort, Heap Sort, Selection Sort

**Why it matters:** When sorting by multiple keys, stable sort preserves the order of previous sorts.

---

### Q15: How do you sort an array of 0s, 1s, and 2s in one pass?

**Answer:**
This is the Dutch National Flag problem (see Q12). The key insight is using three pointers to partition the array into three sections in a single pass.

**Variation — Sort by parity (even/odd):**
```python
def sort_array_by_parity(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] % 2 == 0:
            left += 1
        elif nums[right] % 2 == 1:
            right -= 1
        else:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
    return nums
```

---

## Coding Challenges

### Challenge 1: Sort an Array (Implement Merge Sort)
```python
def sort_array(nums):
    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2
    left = sort_array(nums[:mid])
    right = sort_array(nums[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Test
assert sort_array([5, 2, 3, 1]) == [1, 2, 3, 5]
assert sort_array([5, 1, 1, 2, 0, 0]) == [0, 0, 1, 1, 2, 5]
```
**Time: O(n log n), Space: O(n)**

---

### Challenge 2: Kth Largest Element in an Array
```python
import random


def find_kth_largest(nums, k):
    target = len(nums) - k

    def quickselect(left, right):
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            return quickselect(store + 1, right)
        else:
            return quickselect(left, store - 1)

    return quickselect(0, len(nums) - 1)


# Test
assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
```
**Time: O(n) average, O(n²) worst | O(n) with median-of-medians**

---

### Challenge 3: Sort Colors
```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


# Test
nums = [2, 0, 2, 1, 1, 0]
sort_colors(nums)
assert nums == [0, 0, 1, 1, 2, 2]
```
**Time: O(n), Space: O(1)**

---

### Challenge 4: Merge Intervals
```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# Test
assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
```
**Time: O(n log n), Space: O(n)**

---

### Challenge 5: Meeting Rooms II (Minimum conference rooms)
```python
import heapq


def min_meeting_rooms(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap = [intervals[0][1]]  # End times

    for start, end in intervals[1:]:
        if heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)

    return len(heap)


# Test
assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
assert min_meeting_rooms([[1, 2], [2, 3], [3, 4]]) == 1
```
**Time: O(n log n), Space: O(n)**

---

### Challenge 6: Top K Frequent Elements
```python
from collections import Counter
import heapq


def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)


# Test
assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
assert top_k_frequent([1], 1) == [1]
```
**Time: O(n log k), Space: O(n)**

---

### Challenge 7: Sort Array By Parity
```python
def sort_array_by_parity(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] % 2 == 0:
            left += 1
        elif nums[right] % 2 == 1:
            right -= 1
        else:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
    return nums


# Test
assert sort_array_by_parity([3, 1, 2, 4]) == [4, 2, 1, 3]  # or any valid order
```
**Time: O(n), Space: O(1)**

---

### Challenge 8: Relative Sort Array
Sort arr1 based on the order defined in arr2. Elements not in arr2 go at the end in ascending order.

```python
def relative_sort_array(arr1, arr2):
    order = {val: i for i, val in enumerate(arr2)}

    def custom_sort(x):
        if x in order:
            return (0, order[x])
        return (1, x)

    return sorted(arr1, key=custom_sort)


# Test
assert relative_sort_array([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]) == [
    2,
    2,
    2,
    1,
    4,
    3,
    3,
    9,
    6,
    7,
    19,
]
```
**Time: O(n log n), Space: O(n)**

---

### Challenge 9: Largest Number
Given a list of non-negative integers, arrange them to form the largest number.

```python
from functools import cmp_to_key


def largest_number(nums):
    nums = list(map(str, nums))

    def compare(a, b):
        if a + b > b + a:
            return -1
        elif a + b < b + a:
            return 1
        else:
            return 0

    nums.sort(key=cmp_to_key(compare))
    result = "".join(nums)
    return "0" if result[0] == "0" else result


# Test
assert largest_number([3, 30, 34, 5, 9]) == "9534330"
assert largest_number([10, 2]) == "210"
```
**Time: O(n log n · k)** where k is average string length

---

### Challenge 10: Minimum Absolute Difference
Find all pairs with the minimum absolute difference.

```python
def minimum_abs_difference(arr):
    arr.sort()
    min_diff = float("inf")
    result = []

    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]
        if diff < min_diff:
            min_diff = diff
            result = [[arr[i - 1], arr[i]]]
        elif diff == min_diff:
            result.append([arr[i - 1], arr[i]])

    return result


# Test
assert minimum_abs_difference([4, 2, 1, 3]) == [[1, 2], [2, 3], [3, 4]]
assert minimum_abs_difference([1, 3, 6, 10, 15]) == [[1, 3]]
```
**Time: O(n log n), Space: O(n)**

---

## Common Follow-Up Questions

1. **"Can you do it faster?"** — For comparison-based sorts, O(n log n) is optimal. For integers, use non-comparison sorts.
2. **"Can you sort in O(1) space?"** — Heap Sort, Quick Sort (in-place), some specialized algorithms.
3. **"What about stability?"** — Use Merge Sort or Timsort if stability matters.
4. **"How would you handle very large files?"** — External merge sort (split into chunks, sort each, merge).
5. **"Can you sort a stream of data?"** — Use insertion sort (online), or maintain a heap.
6. **"What's the best general-purpose algorithm?"** — Timsort (Python's default). Quick Sort for in-place.

---

## Tips for Answering Sorting Questions

1. **Know the trade-offs:** Time, space, stability, adaptiveness.
2. **Don't memorize code:** Understand the algorithm and reason about it.
3. **Consider the input:** Small? Large? Nearly sorted? Integers? Linked list?
4. **Mention optimizations:** Random pivot for Quick Sort, insertion sort for small subarrays.
5. **Think about the problem:** Many problems reduce to sorting + one pass.
6. **Python specifics:** `sorted()` is Timsort, stable, O(n log n). `list.sort()` is in-place.

---

## Complexity Cheat Sheet

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix Sort | O(dn) | O(dn) | O(dn) | O(n + k) | Yes |
