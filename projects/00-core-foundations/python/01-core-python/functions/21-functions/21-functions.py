"""
W3Schools Python Tutorial - 21: Python Functions
=================================================
Topics: Defining, calling, parameters, return, args, kwargs, scope, lambda

Run: python 21-functions.py
Reference: https://www.w3schools.com/python/python_functions.asp
"""


# ============================================================
# Defining and Calling Functions
# ============================================================
# Example 1: Basic function
def greet():
    print("Hello, World!")


greet()  # Call the function
# Output: Hello, World!


# Example 2: Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")


greet_person("Alice")
greet_person("Bob")
# Output:
# Hello, Alice!
# Hello, Bob!

# ============================================================
# Parameters vs Arguments
# ============================================================
# Parameters are the variables in the function definition
# Arguments are the values passed to the function


def add(a, b):  # a and b are PARAMETERS
    return a + b


result = add(3, 5)  # 3 and 5 are ARGUMENTS
print(f"\n3 + 5 = {result}")
# Output: 3 + 5 = 8


# ============================================================
# Return Values
# ============================================================
# Example 3: Functions can return values
def multiply(a, b):
    return a * b


result = multiply(4, 5)
print(f"4 * 5 = {result}")


# Example 4: Return multiple values (as tuple)
def getMinMax(numbers):
    return min(numbers), max(numbers)


minimum, maximum = getMinMax([3, 1, 4, 1, 5, 9, 2, 6])
print(f"Min: {minimum}, Max: {maximum}")


# Example 5: Return without value (returns None)
def say_hello():
    print("Hello!")


result = say_hello()
print(f"Return value: {result}")
# Output:
# Hello!
# Return value: None


# ============================================================
# Default Parameters
# ============================================================
# Example 6: Parameters with default values
def greet_with_title(name, title="Mr."):
    print(f"Hello, {title} {name}!")


greet_with_title("Smith")  # Uses default title
greet_with_title("Johnson", "Dr.")  # Custom title

# ⚠️ Default parameters must come after non-default parameters!
# def bad_func(a=1, b):  # SyntaxError!
#     pass


def good_func(a, b=1):  # Correct!
    return a + b


# ============================================================
# *args - Variable Number of Arguments
# ============================================================
# Example 7: Accept any number of positional arguments
def sum_all(*args):
    print(f"args: {args}")
    print(f"type: {type(args)}")
    return sum(args)


result = sum_all(1, 2, 3, 4, 5)
print(f"Sum: {result}")

# Output:
# args: (1, 2, 3, 4, 5)
# type: <class 'tuple'>
# Sum: 15


# Example 8: *args with other parameters
def print_info(name, *hobbies):
    print(f"\n{name}'s hobbies:")
    for hobby in hobbies:
        print(f"  - {hobby}")


print_info("Alice", "reading", "coding", "hiking")


# ============================================================
# **kwargs - Variable Number of Keyword Arguments
# ============================================================
# Example 9: Accept any number of keyword arguments
def print_profile(**kwargs):
    print("Profile:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


print_profile(name="Alice", age=30, city="New York")

# Output:
# Profile:
#   name: Alice
#   age: 30
#   city: New York

# ============================================================
# Scope
# ============================================================
# Example 10: Local vs Global scope
x = "global"  # Global variable


def my_function():
    x = "local"  # Local variable (different from global!)
    print(f"Inside function: x = {x}")


my_function()
print(f"Outside function: x = {x}")

# Output:
# Inside function: x = local
# Outside function: x = global

# Example 11: Using global keyword
counter = 0


def increment():
    global counter
    counter += 1


increment()
increment()
increment()
print(f"\nCounter: {counter}")  # Output: Counter: 3


# ============================================================
# Lambda Functions
# ============================================================
# Example 12: Anonymous functions
# Regular function
def square(x):
    return x**2


# Lambda equivalent
square_lambda = lambda x: x**2

print(f"\nRegular: square(5) = {square(5)}")
print(f"Lambda: square_lambda(5) = {square_lambda(5)}")

# Lambda with multiple arguments
add = lambda a, b: a + b
print(f"Lambda add: {add(3, 5)}")

# Lambda in sorting
students = [("Alice", 90), ("Bob", 80), ("Charlie", 95)]
students.sort(key=lambda s: s[1], reverse=True)
print(f"Students sorted: {students}")

# Lambda in filter and map
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
squares = list(map(lambda x: x**2, numbers))
print(f"Evens: {evens}")
print(f"Squares: {squares}")


# ============================================================
# Recursion
# ============================================================
# Example 13: Recursive function
def factorial(n):
    """Calculate factorial recursively."""
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case


print(f"\nFactorial of 5: {factorial(5)}")  # 120
print(f"Factorial of 10: {factorial(10)}")  # 3628800


# Example 14: Fibonacci with recursion
def fibonacci(n):
    """Return the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print(f"\nFibonacci sequence:")
for i in range(10):
    print(f"  fib({i}) = {fibonacci(i)}")


# ============================================================
# Docstrings
# ============================================================
# Example 15: Documenting functions
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.

    Parameters:
        length (float): The length of the rectangle
        width (float): The width of the rectangle

    Returns:
        float: The area of the rectangle

    Examples:
        >>> calculate_area(5, 3)
        15
        >>> calculate_area(10, 2.5)
        25.0
    """
    return length * width


print(f"\nArea: {calculate_area(5, 3)}")
print(f"Docstring preview: {calculate_area.__doc__}...")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. def function_name(params): define a function")
print("2. return value: send back a result")
print("3. Default params: def func(a, b=10)")
print("4. *args: variable positional arguments (tuple)")
print("5. **kwargs: variable keyword arguments (dict)")
print("6. Scope: local vs global variables")
print("7. Lambda: anonymous functions (lambda x: x + 1)")
print("8. Recursion: function calls itself (need base case!)")
