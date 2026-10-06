"""
Python Practice Problems — NO SOLUTIONS
========================================
Solve these yourself! No hints, no solutions.

Run: python practice_no_solutions.py
Select a problem number to see the description.

Categories:
  EASY (20 XP): Problems 1-41
  MEDIUM (50 XP): Problems 42-81
  HARD (100 XP): Problems 82-99
"""

import math


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Say Hello
# Read a name from input and print a greeting.
# Example: Input "Alice" → Output "Hello, Alice!"
def problem_01():
    name =input("Enter your name : ")
    print(f"Hello,{name}!")
    


# Problem 2: Celsius to Fahrenheit
# Convert a temperature from Celsius to Fahrenheit.
# Formula: F = (C * 9/5) + 32
def problem_02():
    C=float(input("Enter temperature in Celsius : "))
    F = (C * 9/5) + 32
    print(f"{C}°C = {F}°F")


# Problem 3: Even or Odd
# Check if a number is even or odd.
def problem_03():
    num=input("Enter your number")
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")


# Problem 4: Make a Username
# Create a username and initials from a first and last name.
# Example: Input "John Doe" → Username: "john.doe", Initials: "J.D."
def problem_04():
    name=input("Enter your username : ")
    name_lowerd=name.lower()
    name_clean=name_lowerd.split()
    username=f"{name_clean[0]}.{name_clean[1]}"
    intitials=f"{name_clean[0][0].upper()}.{name_clean[1][0].upper}."
    print(f"Username: {username}, Initials: {intitials}")


# Problem 5: Voting Age
# Determine if a person is old enough to vote (18+).
def problem_05():
    """Determine if a person is old enough to vote."""
    age = int(input("Enter your age: "))
    if age >= 18:
        print("You are old enough to vote!")
    else:
        print(f"You need to wait {18 - age} more years to vote.")



# Problem 6: Grade Calculator
# Convert a score into a letter grade:
# 90+ = A, 80-89 = B, 70-79 = C, 60-69 = D, below 60 = F
def problem_06():
    """Convert a score into a letter grade."""
    score = int(input("Enter your score (0-100): "))
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    print(f"Score: {score} → Grade: {grade}")

# Problem 7: Multiplication Table
# Print the multiplication table for a given number (1-10).
def problem_07():
    """Print the multiplication table for a given number """
    num=input("Enter your number: ")
    print(f"Multiplication table for {num}:")
    for i in range(1,int(num)+1):
        print(f"{i}x{num}={i*num}")


# Problem 8: Factorial
# Calculate the factorial of a number (n! = n × (n-1) × ... × 1)
def problem_08():
    """Calculate the factorial of a number."""
    num = int(input("Enter a number: "))
    factorial = 1
    for i in range(1, num + 1):
        factorial *= i
    print(f"{num}! = {factorial}")

# Problem 9: Sum of Numbers
# Read a list of numbers separated by spaces and calculate their sum.
def problem_09():
    """Read a list of numbers and calculate their sum."""
    nums = input("Enter numbers separated by spaces: ")
    numbers = [int(x) for x in nums.split()]
    print(f"Sum: {sum(numbers)}")

# Problem 10: Area Calculator
# Calculate the area of a rectangle, triangle, or circle.
# Rectangle: w × h, Triangle: 0.5 × b × h, Circle: π × r²
def problem_10():
    """Calculate the area of a rectangle, triangle, or circle."""
    shape = input("Enter shape (rectangle/triangle/circle): ").lower()
    if shape == "rectangle":
        w = float(input("Width: "))
        h = float(input("Height: "))
        print(f"Area: {w * h}")
    elif shape == "triangle":
        b = float(input("Base: "))
        h = float(input("Height: "))
        print(f"Area: {0.5 * b * h}")
    elif shape == "circle":
        r = float(input("Radius: "))
        print(f"Area: {math.pi * r ** 2:.2f}")

# Problem 11: Shopping Receipt
# Read item details (name, price, quantity) and print a receipt with total.
def problem_11():
    
    pass  # Write your code here


# Problem 12: Personal Info
# Read name, age, city from input and display them formatted.
def problem_12():
    pass  # Write your code here


# Problem 13: Swap Values
# Read two values and print them in swapped order.
def problem_13():
    pass  # Write your code here


# Problem 14: Rectangle Border
# Print a rectangle border made of stars.
# Example: Width=5, Height=3 →
# *****
# *   *
# *****
def problem_14():
    pass  # Write your code here


# Problem 15: Repeat Message
# Read a message and a number, then print the message that many times.
def problem_15():
    pass  # Write your code here


# Problem 16: Currency Exchange
# Calculate a currency exchange from an amount and rate.
def problem_16():
    pass  # Write your code here


# Problem 17: BMI Calculator
# Calculate Body Mass Index: BMI = weight / height²
# Categories: <18.5 Underweight, 18.5-24.9 Normal, 25-29.9 Overweight, 30+ Obese
def problem_17():
    pass  # Write your code here


# Problem 18: Circle Properties
# Calculate the circumference (2πr) and area (πr²) of a circle.
def problem_18():
    pass  # Write your code here


# Problem 19: Simple Calculator
# Perform basic arithmetic (+, -, *, /) on two numbers.
def problem_19():
    pass  # Write your code here


# Problem 20: Discount Price
# Calculate a discounted price from original price and discount percentage.
def problem_20():
    pass  # Write your code here


# Problem 21: Split the Bill
# Split a total amount equally among a group of people.
def problem_21():
    pass  # Write your code here


# Problem 22: Digit Extractor
# Extract the individual digits of a 3-digit number.
# Example: 123 → Hundreds: 1, Tens: 2, Ones: 3
def problem_22():
    pass  # Write your code here


# Problem 23: Word Counter
# Count the number of words in a sentence.
def problem_23():
    pass  # Write your code here


# Problem 24: Shout It Out
# Convert a string to uppercase and print its length.
def problem_24():
    pass  # Write your code here


# Problem 25: First and Last
# Print the first and last character of a word.
def problem_25():
    pass  # Write your code here


# Problem 26: Repeat String
# Read a string and a number, then print the string repeated that many times.
def problem_26():
    pass  # Write your code here


# Problem 27: Range Checker
# Check if a number falls within a given range.
def problem_27():
    pass  # Write your code here


# Problem 28: Password Check
# Check if a password is at least 8 characters long.
def problem_28():
    pass  # Write your code here


# Problem 29: Ticket Price
# Determine ticket price based on age:
# <5 Free, 5-11 Child $5, 12-59 Adult $10, 60+ Senior $7
def problem_29():
    pass  # Write your code here


# Problem 30: Positive Negative Zero
# Check if a number is positive, negative, or zero.
def problem_30():
    pass  # Write your code here


# Problem 31: Smallest of Three
# Find the smallest of three numbers.
def problem_31():
    pass  # Write your code here


# Problem 32: Countdown
# Count down from a number to 1, then print "Go!"
def problem_32():
    pass  # Write your code here


# Problem 33: FizzBuzz
# For numbers 1 to N:
# - If divisible by 3 and 5: print "FizzBuzz"
# - If divisible by 3: print "Fizz"
# - If divisible by 5: print "Buzz"
# - Otherwise: print the number
def problem_33():
    pass  # Write your code here


# Problem 34: Sum 1 to N
# Calculate the sum of all numbers from 1 to N.
def problem_34():
    pass  # Write your code here


# Problem 35: Star Triangle
# Print a right triangle made of stars.
# Example: Height=4 →
# *
# **
# ***
# ****
def problem_35():
    pass  # Write your code here


# Problem 36: Tip Calculator
# Calculate tip amount and total bill from bill amount and tip percentage.
def problem_36():
    pass  # Write your code here


# Problem 37: Power Function
# Calculate the power of a number (base^exponent).
def problem_37():
    pass  # Write your code here


# Problem 38: Average Score
# Read a list of scores and calculate their average.
def problem_38():
    pass  # Write your code here


# Problem 39: Count Matches
# Count how many numbers in a list match a target value.
def problem_39():
    pass  # Write your code here


# Problem 40: Min and Max
# Find the smallest and largest numbers in a list.
def problem_40():
    pass  # Write your code here


# Problem 41: Absolute Difference
# Calculate the absolute difference between two numbers.
def problem_41():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 42: Leap Year
# Determine if a year is a leap year:
# - Divisible by 4 AND (not divisible by 100 OR divisible by 400)
def problem_42():
    pass  # Write your code here


# Problem 43: Day of Week
# Convert a day number (1-7) to a day name (Monday-Sunday).
def problem_43():
    pass  # Write your code here


# Problem 44: Triangle Classifier
# Classify a triangle by side lengths:
# - All equal: Equilateral
# - Two equal: Isosceles
# - All different: Scalene
# - Invalid if sum of two sides <= third side
def problem_44():
    pass  # Write your code here


# Problem 45: Time Converter
# Convert seconds to hours, minutes, and seconds.
# Example: 3661 → 1h 1m 1s
def problem_45():
    pass  # Write your code here


# Problem 46: Reverse Words
# Reverse the order of words in a sentence.
# Example: "Hello World" → "World Hello"
def problem_46():
    pass  # Write your code here


# Problem 47: Palindrome Check
# Check if a word reads the same forwards and backwards.
# Example: "racecar" → True, "hello" → False
def problem_47():
    pass  # Write your code here


# Problem 48: Count Vowels
# Count the number of vowels (a, e, i, o, u) in a string.
def problem_48():
    pass  # Write your code here


# Problem 49: Title Case
# Capitalize the first letter of each word in a sentence.
def problem_49():
    pass  # Write your code here


# Problem 50: Remove Consecutive Duplicates
# Remove consecutive duplicate characters from a string.
# Example: "aabbcc" → "abc", "aabbc" → "abc"
def problem_50():
    pass  # Write your code here


# Problem 51: Longest Word
# Find the longest word in a sentence.
def problem_51():
    pass  # Write your code here


# Problem 52: Access Control
# Determine access based on:
# - Admin: always granted
# - User + member + age>=18: granted
# - User + age>=21: granted
# - Otherwise: denied
def problem_52():
    pass  # Write your code here


# Problem 53: Digit Sum
# Calculate the sum of all digits in a number.
# Example: 1234 → 1+2+3+4 = 10
def problem_53():
    pass  # Write your code here


# Problem 54: Number Pyramid
# Print a pyramid of numbers.
# Example: Height=4 →
#    1
#   1 2
#  1 2 3
# 1 2 3 4
def problem_54():
    pass  # Write your code here


# Problem 55: Collatz Steps
# Count steps to reach 1 using Collatz sequence:
# - If even: divide by 2
# - If odd: multiply by 3 and add 1
def problem_55():
    pass  # Write your code here


# Problem 56: Prime Check
# Check if a number is a prime number.
def problem_56():
    pass  # Write your code here


# Problem 57: Reverse Number
# Reverse the digits of a number.
# Example: 1234 → 4321
def problem_57():
    pass  # Write your code here


# Problem 58: Is Palindrome Function
# Write a function that checks if a word is a palindrome.
def problem_58():
    pass  # Write your code here


# Problem 59: Min of Three
# Write a function that returns the smallest of three numbers.
def problem_59():
    pass  # Write your code here


# Problem 60: Count Digits
# Count the number of digits in a number.
# Example: 12345 → 5
def problem_60():
    pass  # Write your code here


# Problem 61: Recursive Sum
# Write a recursive function to sum numbers from 1 to N.
def problem_61():
    pass  # Write your code here


# Problem 62: Array Map Function
# Write a function that doubles every number in a list.
# Example: [1,2,3] → [2,4,6]
def problem_62():
    pass  # Write your code here


# Problem 63: Find the Largest
# Read a list of numbers and find the largest one.
def problem_63():
    pass  # Write your code here


# Problem 64: Reverse a List
# Read a list of numbers and print them in reverse order.
def problem_64():
    pass  # Write your code here


# Problem 65: Second Largest
# Find the second largest number in a list.
def problem_65():
    pass  # Write your code here


# Problem 66: Running Sum
# Print the running (cumulative) sum of a list.
# Example: [1,2,3,4] → [1,3,6,10]
def problem_66():
    pass  # Write your code here


# Problem 67: Count Above Average
# Count how many numbers in a list are above the average.
def problem_67():
    pass  # Write your code here


# Problem 68: Longest Streak
# Find the longest consecutive streak of the same number.
# Example: [1,1,2,2,2,3] → 3 (three 2s in a row)
def problem_68():
    pass  # Write your code here


# Problem 69: Greatest Common Divisor
# Find the GCD of two numbers.
# Example: GCD(12, 8) = 4
def problem_69():
    pass  # Write your code here


# Problem 70: Fibonacci
# Print the first N numbers of the Fibonacci sequence.
# Example: N=6 → [0, 1, 1, 2, 3, 5]
def problem_70():
    pass  # Write your code here


# Problem 71: Prime Factors
# Find all prime factors of a number.
# Example: 12 → [2, 2, 3]
def problem_71():
    pass  # Write your code here


# Problem 72: Power of Two
# Check if a number is a power of 2.
# Example: 8 → True, 6 → False
def problem_72():
    pass  # Write your code here


# Problem 73: Sum of Squares
# Calculate the sum of squares from 1 to N.
# Example: N=3 → 1²+2²+3² = 14
def problem_73():
    pass  # Write your code here


# Problem 74: LCM Calculator
# Calculate the least common multiple of two numbers.
# Example: LCM(4, 6) = 12
def problem_74():
    pass  # Write your code here


# Problem 75: Perfect Number
# Check if a number is a perfect number.
# A perfect number equals the sum of its proper divisors.
# Example: 6 = 1+2+3 → True
def problem_75():
    pass  # Write your code here


# Problem 76: Sort Three Numbers
# Read three numbers and print them in ascending order.
def problem_76():
    pass  # Write your code here


# Problem 77: Sort Numbers
# Read a list of numbers and print them sorted.
def problem_77():
    pass  # Write your code here


# Problem 78: Sort Words
# Read a list of words and print them sorted alphabetically.
def problem_78():
    pass  # Write your code here


# Problem 79: Letter Frequency
# Count how many times each letter appears in a word.
def problem_79():
    pass  # Write your code here


# Problem 80: Most Common Char
# Find the character that appears most often in a string.
def problem_80():
    pass  # Write your code here


# Problem 81: Digit Frequency
# Count how many times each digit appears in a number.
def problem_81():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 82: Caesar Cipher
# Encrypt a message by shifting each letter in the alphabet.
# Example: "hello" with shift 3 → "khoor"
def problem_82():
    pass  # Write your code here


# Problem 83: Anagram Check
# Check if two words are anagrams (same letters, different order).
# Example: "listen" and "silent" → True
def problem_83():
    pass  # Write your code here


# Problem 84: Run Length Encoding
# Compress a string using run-length encoding.
# Example: "aaabbbcc" → "a3b3c2"
def problem_84():
    pass  # Write your code here


# Problem 85: Date Validator
# Check if a given date (DD/MM/YYYY) is valid.
# Consider: month range, days in month, leap years.
def problem_85():
    pass  # Write your code here


# Problem 86: Diamond Pattern
# Print a diamond pattern of stars.
# Example: Half height=3 →
#   *
#  ***
# *****
#  ***
#   *
def problem_86():
    pass  # Write your code here


# Problem 87: Number to Binary
# Convert a decimal number to binary.
# Example: 10 → "1010"
def problem_87():
    pass  # Write your code here


# Problem 88: Pascal Triangle Row
# Print a specific row of Pascal's triangle.
# Example: Row 4 → [1, 4, 6, 4, 1]
def problem_88():
    pass  # Write your code here


# Problem 89: Remove Duplicates (List)
# Remove duplicate numbers from a list while keeping order.
# Example: [1,2,2,3,1] → [1,2,3]
def problem_89():
    pass  # Write your code here


# Problem 90: Rotate Left
# Rotate a list of numbers to the left by K positions.
# Example: [1,2,3,4,5] rotated by 2 → [3,4,5,1,2]
def problem_90():
    pass  # Write your code here


# Problem 91: Merge Sorted
# Merge two sorted lists into one sorted list.
def problem_91():
    pass  # Write your code here


# Problem 92: Pair Sum
# Find the first pair of numbers that add up to a target.
# Example: [2,7,11,15], target=9 → [2,7]
def problem_92():
    pass  # Write your code here


# Problem 93: GCD Function (Recursive)
# Write a recursive function to find the GCD of two numbers.
def problem_93():
    pass  # Write your code here


# Problem 94: Number Base Convert
# Convert a number from one base to another.
# Example: 10 (base 10) → 1010 (base 2)
def problem_94():
    pass  # Write your code here


# Problem 95: Bubble Sort
# Implement bubble sort and count the number of swaps.
def problem_95():
    pass  # Write your code here


# Problem 96: Selection Sort
# Implement selection sort and print each step.
def problem_96():
    pass  # Write your code here


# Problem 97: Insertion Sort
# Implement insertion sort and print each step.
def problem_97():
    pass  # Write your code here


# Problem 98: Word Frequency
# Count how many times each word appears in a sentence.
def problem_98():
    pass  # Write your code here


# Problem 99: Unique Elements Count
# Count how many unique numbers appear in a list.
# Example: [1,2,2,3,3,3] → 3 unique
def problem_99():
    pass  # Write your code here


# ============================================================
# MAIN MENU
# ============================================================

def main():
    problems = {
        # Easy
        1: "Say Hello",
        2: "Celsius to Fahrenheit",
        3: "Even or Odd",
        4: "Make a Username",
        5: "Voting Age",
        6: "Grade Calculator",
        7: "Multiplication Table",
        8: "Factorial",
        9: "Sum of Numbers",
        10: "Area Calculator",
        11: "Shopping Receipt",
        12: "Personal Info",
        13: "Swap Values",
        14: "Rectangle Border",
        15: "Repeat Message",
        16: "Currency Exchange",
        17: "BMI Calculator",
        18: "Circle Properties",
        19: "Simple Calculator",
        20: "Discount Price",
        21: "Split the Bill",
        22: "Digit Extractor",
        23: "Word Counter",
        24: "Shout It Out",
        25: "First and Last",
        26: "Repeat String",
        27: "Range Checker",
        28: "Password Check",
        29: "Ticket Price",
        30: "Positive Negative Zero",
        31: "Smallest of Three",
        32: "Countdown",
        33: "FizzBuzz",
        34: "Sum 1 to N",
        35: "Star Triangle",
        36: "Tip Calculator",
        37: "Power Function",
        38: "Average Score",
        39: "Count Matches",
        40: "Min and Max",
        41: "Absolute Difference",
        # Medium
        42: "Leap Year",
        43: "Day of Week",
        44: "Triangle Classifier",
        45: "Time Converter",
        46: "Reverse Words",
        47: "Palindrome Check",
        48: "Count Vowels",
        49: "Title Case",
        50: "Remove Consecutive Duplicates",
        51: "Longest Word",
        52: "Access Control",
        53: "Digit Sum",
        54: "Number Pyramid",
        55: "Collatz Steps",
        56: "Prime Check",
        57: "Reverse Number",
        58: "Is Palindrome Function",
        59: "Min of Three",
        60: "Count Digits",
        61: "Recursive Sum",
        62: "Array Map Function",
        63: "Find the Largest",
        64: "Reverse a List",
        65: "Second Largest",
        66: "Running Sum",
        67: "Count Above Average",
        68: "Longest Streak",
        69: "Greatest Common Divisor",
        70: "Fibonacci",
        71: "Prime Factors",
        72: "Power of Two",
        73: "Sum of Squares",
        74: "LCM Calculator",
        75: "Perfect Number",
        76: "Sort Three Numbers",
        77: "Sort Numbers",
        78: "Sort Words",
        79: "Letter Frequency",
        80: "Most Common Char",
        81: "Digit Frequency",
        # Hard
        82: "Caesar Cipher",
        83: "Anagram Check",
        84: "Run Length Encoding",
        85: "Date Validator",
        86: "Diamond Pattern",
        87: "Number to Binary",
        88: "Pascal Triangle Row",
        89: "Remove Duplicates (List)",
        90: "Rotate Left",
        91: "Merge Sorted",
        92: "Pair Sum",
        93: "GCD Function (Recursive)",
        94: "Number Base Convert",
        95: "Bubble Sort",
        96: "Selection Sort",
        97: "Insertion Sort",
        98: "Word Frequency",
        99: "Unique Elements Count",
    }

    print("=" * 50)
    print("  Python Practice Problems — NO SOLUTIONS")
    print("=" * 50)
    print("\n  SOLVE THESE YOURSELF!")
    print("  No hints, no solutions provided.")
    print("\nCategories:")
    print("  EASY (1-41):    20 XP each")
    print("  MEDIUM (42-81): 50 XP each")
    print("  HARD (82-99):   100 XP each")
    print("\n  Type 'list' to see all problems")
    print("  Type 'quit' to exit")
    print("=" * 50)

    while True:
        choice = input("\nEnter problem number: ").strip().lower()

        if choice == "quit":
            print("Goodbye!")
            break
        elif choice == "list":
            print("\n--- EASY ---")
            for num in range(1, 42):
                print(f"  {num:2d}. {problems[num]}")
            print("\n--- MEDIUM ---")
            for num in range(42, 82):
                print(f"  {num:2d}. {problems[num]}")
            print("\n--- HARD ---")
            for num in range(82, 100):
                print(f"  {num:2d}. {problems[num]}")
            continue

        try:
            num = int(choice)
            if num in problems:
                print(f"\n--- Problem {num}: {problems[num]} ---")
                print(f"\nRead the description in the source code.")
                print(f"Open: projects/00-core-foundations/python/practice_no_solutions.py")
                print(f"Find: def problem_{num:02d}()")
                print(f"Write your solution in the function body.")
                print(f"\nWhen done, test it by running the function!")
            else:
                print("Invalid problem number. Enter 1-99.")
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
