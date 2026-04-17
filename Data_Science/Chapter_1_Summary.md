# Chapter 1: Basic Math and Calculus Review

## Overview
This chapter provides a practical review of essential mathematical concepts needed for data science work. It focuses on the specific mathematical foundations that underpin machine learning algorithms and statistical computing.

---

## 1. Number Theory

### What is Number Theory?
Number theory studies different number systems and why we have accepted them as we do today. It explains the foundations of our numbering system.

### Types of Numbers in Data Science

**Natural Numbers**
- Definition: Positive counting numbers (1, 2, 3, 4, 5...)
- Historical context: Earliest known number system, used by cavemen for tally marks
- Data science application: Counting observations, samples, iterations, categorical IDs

**Whole Numbers**
- Definition: Natural numbers plus zero (0, 1, 2, 3...)
- Historical context: Developed by Babylonians for place-holding notation
- Importance: Zero represents missing values, baseline measurements, indexing operations
- Data science application: Normalization factors, probability values, discrete feature values

**Integers**
- Definition: Whole numbers and their negatives (-∞, ..., -2, -1, 0, 1, 2, ...)
- Historical context: Ancient mathematicians distrusted negative numbers until Brahmagupta (628 AD) proved their necessity for quadratic formula
- Data science application: Financial calculations (profits/losses), index offsets, array indices, categorical encodings

**Rational Numbers**
- Definition: Numbers expressible as fractions (p/q where q ≠ 0)
- Examples: 2/3, 0.5, 687/100 = 6.87, 2/1 = 2
- Includes: All finite decimals and integers
- Data science application: Normalization factors, probability values, precision measurements, rate calculations

**Irrational Numbers**
- Definition: Cannot be expressed as fractions
- Examples: π (pi), √2, e (Euler's number)
- Characteristics: Infinite non-repeating decimal expansions
- Historical note: Greek mathematician Pythagoras believed all numbers were rational until Hippasus proved √2 is irrational
- Data science application: Circular data (angles, time periods), exponential growth models, standardized scores (z-scores), trigonometric functions

**Real Numbers**
- Definition: Both rational and irrational numbers
- Data science application: Primary number type used for continuous variables, measurements, normalized values, decimal representations

**Complex and Imaginary Numbers**
- Definition: Numbers involving imaginary unit i (√-1)
- Data science application: Advanced cases like Fourier transforms, certain matrix decompositions, quantum computing
- Note: Generally not required for most data science tasks

### Key Takeaway for Data Science
Most data science work involves whole numbers, natural numbers, integers, and real numbers. Understanding these types helps in:
- Selecting appropriate data types in Python (int, float)
- Handling categorical vs. continuous variables
- Understanding precision and rounding requirements
- Designing data storage and compression strategies

---

## 2. Order of Operations (PEMDAS)

### The Hierarchy
Mathematical expressions are evaluated in a specific order:
1. **P**arentheses
2. **E**xponents
3. **M**ultiplication and **D**ivision (left to right)
4. **A**ddition and **S**ubtraction (left to right)

### Example Expression
```
2 * (3 + 2)**2 / 5 - 4
```

**Step-by-step evaluation:**
1. Evaluate parentheses: (3 + 2) = 5
2. Solve exponent: 5² = 25
3. Multiplication: 2 * 25 = 50
4. Division: 50 / 5 = 10
5. Subtraction: 10 - 4 = 6

### Python Implementation

**Example 1: Basic expression**
```python
my_value = 2 * (3 + 2)**2 / 5 - 4 
print(my_value)  # prints 6.0
```

**Example 2: With explicit parentheses for clarity**
```python
my_value = 2 * ((3 + 2)**2 / 5) - 4 
print(my_value)  # prints 6.0
```

### Data Science Importance
Proper order of operations is critical for:
- **Complex formula evaluation**: Machine learning formulas often involve multiple operations
- **Numerical stability**: Incorrect order can lead to floating-point errors
- **Reproducibility**: Clear operation order ensures consistent results
- **Code readability**: Explicit parentheses prevent bugs when others modify code

**Best Practice**: Always use parentheses liberally in complex expressions to establish clear evaluation order.

---

## 3. Variables

### Definition in Mathematics
A variable is a named placeholder for an unspecified or unknown number.

### Python Implementation
Direct mapping from mathematical variables to Python variables.

### Example
```python
# Take a variable input x and multiply it by 3
x = int(input("Please input a number\n")) 
product = 3 * x 
print(product)
```

### Standard Variable Names
- **θ (theta)**: Often represents angles or parameters
- **β (beta)**: Typically a parameter in linear regression
- **α (alpha)**: Learning rate, intercept
- **μ (mu)**: Population mean
- **σ (sigma)**: Population standard deviation

### Note on Python
Greek symbols make awkward variable names in Python, so we typically name these variables `theta`, `beta`, `alpha`, `mu`, `sigma` instead of using the actual symbols.

### Data Science Application
Variables are fundamental for:
- **Model representation**: Machine learning models as mathematical functions
- **Feature engineering**: Creating new features as functions of existing ones
- **Parameter tuning**: Adjusting model hyperparameters
- **Result interpretation**: Understanding what each variable represents

---

## 4. Functions (Coming in next sections)

This section introduces the concept of functions, which represent relationships between inputs and outputs. In data science:
- Machine learning models are mathematical functions
- Loss functions are objective functions to minimize/maximize
- Activation functions are non-linear transformations
- Transformation functions scale, normalize, or encode data

---

## Summary

Chapter 1 establishes the foundational math concepts needed for the rest of the book:
1. **Number Theory**: Understanding different types of numbers and their applications
2. **Order of Operations**: Critical for complex formula evaluation in code
3. **Variables**: Foundation for mathematical modeling in data science
4. **Functions**: Essential for representing machine learning models

These concepts are not meant to be a comprehensive math crash course, but rather to provide the essential mathematical foundations needed to understand data science tools and machine learning algorithms.

**Philosophy**: Python does the heavy lifting numerically, but understanding the math helps you:
- Debug machine learning models
- Choose appropriate algorithms
- Interpret results correctly
- Ask critical questions about "black box" tools
- Understand the mathematics behind data science applications

**Next Chapters**:
- Chapter 2: Exponents and Logarithms
- Chapter 3: Derivatives and Integrals (Calculus)
- Chapter 4: Applied areas of essential math (probability, linear algebra, statistics)
- Later chapters: Machine learning techniques integrating all concepts

---

*This chapter sets the foundation for understanding the mathematics behind data science tools and machine learning algorithms. The concepts reviewed here will be applied throughout the rest of the book.*