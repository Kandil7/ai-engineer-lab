# DSA Linked Lists Interview Practice

## Topic Overview

Linked lists store elements in nodes where each node points to the next. Unlike arrays, they allow O(1) insertion/deletion at known positions but O(n) access. Interviews heavily test pointer manipulation, cycle detection, and reversal.

**Key Properties:**
- Non-contiguous memory allocation
- O(n) access by index (no random access)
- O(1) insertion/deletion at head
- O(n) insertion/deletion at arbitrary position (need to traverse)
- Extra memory for pointers (8 bytes per node on 64-bit)

**Types:**
- **Singly linked list:** Each node → next
- **Doubly linked list:** Each node → prev, next
- **Circular linked list:** Last node → head

---

## Interview Questions (with Answers)

### Q1: What are the advantages and disadvantages of linked lists over arrays?

**Answer:**

| Aspect | Linked List | Array |
|--------|-------------|-------|
| Access by index | O(n) | O(1) |
| Insert at beginning | O(1) | O(n) |
| Insert at end | O(1) amortized | O(1) amortized |
| Insert at middle | O(1) if at position | O(n) |
| Delete | O(1) if at node | O(n) |
| Memory | Extra pointer overhead | Contiguous, cache-friendly |
| Cache performance | Poor | Excellent |

**When to use linked lists:** Frequent insertions/deletions at known positions, unknown size, implementing stacks/queues with dynamic size.

---

### Q2: Explain the fast and slow pointer technique (Floyd's algorithm).

**Answer:**
Two pointers move at different speeds. The fast pointer moves 2 steps, slow moves 1 step. If there's a cycle, they will meet.

**Cycle detection:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Find cycle start:**
```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Reset one pointer to head
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

**Why the cycle start works:** After detecting the cycle meeting point, the distance from head to cycle start equals the distance from meeting point to cycle start (moving around the cycle).

---

### Q3: How do you reverse a linked list?

**Answer:**
**Iterative approach (O(n) time, O(1) space):**
```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```

**Recursive approach (O(n) time, O(n) stack space):**
```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

### Q4: How do you find the middle of a linked list?

**Answer:**
Fast/slow pointer — fast moves 2 steps, slow moves 1 step. When fast reaches the end, slow is at the middle.

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**For even-length lists:** Returns the second middle (for [1,2,3,4], returns 3). To get the first middle, use `fast = head.next` initially.

---

### Q5: How do you merge two sorted linked lists?

**Answer:**
```python
def merge_two_lists(l1, l2):
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

**Time: O(n + m), Space: O(1)**

---

### Q6: How do you detect a cycle and find its length?

**Answer:**
```python
def cycle_length(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Count cycle length
            length = 1
            fast = fast.next
            while slow != fast:
                fast = fast.next
                length += 1
            return length
    return 0
```

---

### Q7: How do you remove the Nth node from the end?

**Answer:**
Two-pointer technique — advance the first pointer n steps, then move both until the first reaches the end.

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy

    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next

    # Skip the nth node
    slow.next = slow.next.next
    return dummy.next
```

**Time: O(L), Space: O(1)** where L is the list length.

---

### Q8: How do you check if a linked list is a palindrome?

**Answer:**
**Approach: Reverse second half and compare**
```python
def is_palindrome(head):
    if not head or not head.next:
        return True

    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node

    # Compare
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True
```

**Time: O(n), Space: O(1)**

---

### Q9: How do you copy a linked list with a random pointer?

**Answer:**
**Hash map approach (O(n) time, O(n) space):**
```python
def copy_random_list(head):
    if not head:
        return None

    mapping = {}
    curr = head
    while curr:
        mapping[curr] = Node(curr.val)
        curr = curr.next

    curr = head
    while curr:
        if curr.next:
            mapping[curr].next = mapping[curr.next]
        if curr.random:
            mapping[curr].random = mapping[curr.random]
        curr = curr.next

    return mapping[head]
```

**Interleaving approach (O(n) time, O(1) space):**
Insert copy nodes between originals, set random pointers, then separate.

---

### Q10: How do you flatten a multilevel doubly linked list?

**Answer:**
DFS approach — when encountering a child, recurse on it before continuing with next.

```python
def flatten(head):
    if not head:
        return head

    curr = head
    while curr:
        if curr.child:
            # Flatten the child list
            child_head = flatten(curr.child)
            child_tail = child_head
            while child_tail.next:
                child_tail = child_tail.next

            # Connect
            next_node = curr.next
            curr.next = child_head
            child_head.prev = curr
            child_tail.next = next_node
            if next_node:
                next_node.prev = child_tail

            curr.child = None
        curr = curr.next

    return head
```

---

### Q11: How do you add two numbers represented as linked lists?

**Answer:**
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        val = carry
        if l1:
            val += l1.val
            l1 = l1.next
        if l2:
            val += l2.val
            l2 = l2.next
        carry, digit = divmod(val, 10)
        curr.next = ListNode(digit)
        curr = curr.next

    return dummy.next
```

**Example:** 342 + 465 = 807 → [2,4,3] + [5,6,4] = [7,0,8]

---

### Q12: How do you swap nodes in pairs?

**Answer:**
```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next and prev.next.next:
        first = prev.next
        second = first.next

        first.next = second.next
        second.next = first
        prev.next = second

        prev = first

    return dummy.next
```

**Time: O(n), Space: O(1)**

---

### Q13: How do you reorder a linked list L0→L1→…→Ln-1→Ln to L0→Ln→L1→Ln-1→…?

**Answer:**
Three-step approach:
1. Find middle using fast/slow pointers
2. Reverse second half
3. Merge two halves alternately

```python
def reorder_list(head):
    if not head or not head.next:
        return

    # Find middle
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev, curr = None, slow.next
    slow.next = None
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # Merge
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2
```

---

### Q14: What is the difference between singly and doubly linked lists?

**Answer:**

| Feature | Singly | Doubly |
|---------|--------|--------|
| Direction | Forward only | Forward and backward |
| Memory | Less (one pointer) | More (two pointers) |
| Delete given node | Need previous node | Can delete directly |
| Insert before | Need traversal | O(1) with pointer |
| Use cases | Stacks, simple queues | LRU cache, browser history |

---

### Q15: How do you find the intersection point of two linked lists?

**Answer:**
**Two-pointer approach:**
```python
def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None

    pA, pB = headA, headB
    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA

    return pA
```

**Why it works:** Both pointers traverse len(A) + len(B) steps. If they intersect, they meet at the intersection point. If not, they both become None simultaneously.

---

## Coding Challenges

### Challenge 1: Reverse a Linked List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


# Helper: build list from array
def build_list(arr):
    dummy = ListNode(0)
    curr = dummy
    for val in arr:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next


# Helper: list to array
def to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# Test
head = build_list([1, 2, 3, 4, 5])
assert to_array(reverse_list(head)) == [5, 4, 3, 2, 1]
```
**Time: O(n), Space: O(1)**

---

### Challenge 2: Merge Two Sorted Lists
```python
def merge_two_lists(l1, l2):
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


# Test
l1 = build_list([1, 2, 4])
l2 = build_list([1, 3, 4])
assert to_array(merge_two_lists(l1, l2)) == [1, 1, 2, 3, 4, 4]
```
**Time: O(n + m), Space: O(1)**

---

### Challenge 3: Linked List Cycle
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


# Test
head = build_list([3, 2, 0, -4])
head.next.next.next.next = head.next  # Create cycle
assert has_cycle(head) == True

head = build_list([1, 2])
assert has_cycle(head) == False
```
**Time: O(n), Space: O(1)**

---

### Challenge 4: Remove Nth Node From End
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy

    for _ in range(n + 1):
        fast = fast.next

    while fast:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
    return dummy.next


# Test
head = build_list([1, 2, 3, 4, 5])
assert to_array(remove_nth_from_end(head, 2)) == [1, 2, 3, 5]

head = build_list([1])
assert to_array(remove_nth_from_end(head, 1)) == []
```
**Time: O(L), Space: O(1)**

---

### Challenge 5: Reverse Linked List II (Reverse from position m to n)
```python
def reverse_between(head, m, n):
    if not head or m == n:
        return head

    dummy = ListNode(0, head)
    prev = dummy

    # Move to position m
    for _ in range(m - 1):
        prev = prev.next

    curr = prev.next
    for _ in range(n - m):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next


# Test
head = build_list([1, 2, 3, 4, 5])
assert to_array(reverse_between(head, 2, 4)) == [1, 4, 3, 2, 5]
```
**Time: O(n), Space: O(1)**

---

### Challenge 6: Add Two Numbers
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        val = carry
        if l1:
            val += l1.val
            l1 = l1.next
        if l2:
            val += l2.val
            l2 = l2.next
        carry, digit = divmod(val, 10)
        curr.next = ListNode(digit)
        curr = curr.next

    return dummy.next


# Test
l1 = build_list([2, 4, 3])
l2 = build_list([5, 6, 4])
assert to_array(add_two_numbers(l1, l2)) == [7, 0, 8]
```
**Time: O(max(m, n)), Space: O(max(m, n))**

---

### Challenge 7: Copy List with Random Pointer
```python
class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head):
    if not head:
        return None

    mapping = {}
    curr = head
    while curr:
        mapping[curr] = RandomNode(curr.val)
        curr = curr.next

    curr = head
    while curr:
        if curr.next:
            mapping[curr].next = mapping[curr.next]
        if curr.random:
            mapping[curr].random = mapping[curr.random]
        curr = curr.next

    return mapping[head]
```
**Time: O(n), Space: O(n)**

---

### Challenge 8: Flatten a Multilevel Linked List
```python
def flatten(head):
    if not head:
        return head

    curr = head
    while curr:
        if curr.child:
            child_head = flatten(curr.child)
            child_tail = child_head
            while child_tail.next:
                child_tail = child_tail.next

            next_node = curr.next
            curr.next = child_head
            child_head.prev = curr
            child_tail.next = next_node
            if next_node:
                next_node.prev = child_tail

            curr.child = None
        curr = curr.next

    return head
```
**Time: O(n), Space: O(d)** where d is max depth (recursion stack)

---

### Challenge 9: LRU Cache
```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)
assert cache.get(2) == -1
```
**Time: O(1) for both operations, Space: O(capacity)**

---

### Challenge 10: Partition List
Given a linked list and value x, partition so all nodes < x come before nodes >= x.

```python
def partition(head, x):
    less_head = ListNode(0)
    greater_head = ListNode(0)
    less = less_head
    greater = greater_head

    while head:
        if head.val < x:
            less.next = head
            less = less.next
        else:
            greater.next = head
            greater = greater.next
        head = head.next

    greater.next = None
    less.next = greater_head.next
    return less_head.next


# Test
head = build_list([1, 4, 3, 2, 5, 2])
assert to_array(partition(head, 3)) == [1, 2, 2, 4, 3, 5]
```
**Time: O(n), Space: O(1)**

---

## Common Follow-Up Questions

1. **"Can you do it without extra space?"** — Most linked list problems can be solved in O(1) space with pointer manipulation.
2. **"What if the list has a cycle?"** — Use Floyd's algorithm for detection, or handle the cycle explicitly.
3. **"What about very long lists?"** — Iterative approaches are preferred over recursive (stack overflow risk).
4. **"How would you handle duplicates?"** — Depends on the problem; usually just skip or merge as needed.
5. **"Can you use a hash map?"** — Yes, but it's O(n) space. Pointers are usually O(1).
6. **"What's the time complexity of inserting at a known node?"** — O(1) if you have the node reference, O(n) if you need to find it.

---

## Tips for Answering Linked List Questions

1. **Draw the pointers:** Sketch the list and pointer movements on paper or a whiteboard.
2. **Use a dummy node:** Simplifies edge cases (head deletion, merging).
3. **Handle null checks:** Always check for empty lists and single-node lists.
4. **Think about in-place:** Most linked list problems want O(1) space.
5. **Practice pointer manipulation:** The key skill is updating `next` pointers correctly.
6. **Know the patterns:** Fast/slow pointers, dummy nodes, reversal, two-pointer merge.
7. **State the complexity:** Both time and space complexity for each approach.

---

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| Reverse List | O(n) | O(1) iterative, O(n) recursive |
| Detect Cycle | O(n) | O(1) |
| Find Middle | O(n) | O(1) |
| Merge Sorted Lists | O(n+m) | O(1) |
| Remove Nth from End | O(L) | O(1) |
| Check Palindrome | O(n) | O(1) |
| Copy with Random | O(n) | O(n) |
| Add Two Numbers | O(max(m,n)) | O(max(m,n)) |
| Flatten | O(n) | O(d) recursion |
| LRU Cache | O(1) | O(capacity) |
