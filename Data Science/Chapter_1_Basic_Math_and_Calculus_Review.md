# Chapter 1: Basic Math and Calculus Review

*Essential Math for Data Science by Thomas Nield (O'Reilly Media, 2022)*

## Chapter Overview

This chapter serves as a foundational review of basic mathematics and calculus concepts that will be essential for understanding the "black box" of machine learning algorithms. The chapter covers number theory, order of operations, variables, functions, exponents, logarithms, derivatives, and integrals - all with practical Python implementations.

**Important Note:** This is NOT a comprehensive math crash course. It focuses specifically on the essential math needed for data science work.

---

## 1. Number Theory: Understanding Numbers

### 1.1 Number Systems

#### Natural Numbers (ℕ)
- **Definition**: The counting numbers: 1, 2, 3, 4, 5...
- **History**: The earliest number system, dating back to ancient tally marks
- **Use in Data Science**: Basic counting and iteration

#### Whole Numbers (ℕ₀)
- **Definition**: Natural numbers plus zero: 0, 1, 2, 3, 4...
- **Significance**: Introduces the concept of "nothing" and place-holding notation
- **Historical Context**: Babylonians developed place-holder notation

#### Integers (ℤ)
- **Definition**: Positive and negative whole numbers including zero
- **Why Negative Numbers Matter**: Essential for finances (profits/losses)
- **Historical Note**: Indian mathematician Brahmagupta (628 AD) formalized negative numbers

#### Rational Numbers (ℚ)
- **Definition**: Numbers expressible as fractions (p/q where q ≠ 0)
- **Includes**: All finite decimals and integers
  - Example: 6.87 = 687/100
  - Example: 2 = 2/1
- **Practical Use**: Time, resources, and measurements often require fractional units
  - Example: Running 9/10 of a mile, measuring 1/2 gallon of milk

#### Irrational Numbers
- **Definition**: Numbers that cannot be expressed as fractions
- **Examples**: 
  - π (pi) = 3.141592653589793238462...
  - √2 = 1.41421356...
  - e (Euler's number) = 2.718281828...
- **Characteristics**: Infinite non-repeating decimal digits
- **Historical Legend**: Pythagoras believed all numbers were rational. His follower Hippasus proved √2 is irrational, leading to Pythagoras's legendary (alleged) drowning.

#### Real Numbers (ℝ)
- **Definition**: The union of rational and irrational numbers
- **Data Science Context**: All decimal numbers encountered in data science are real numbers
- **Practical Application**: The foundation for continuous variables in statistics and machine learning

#### Complex and Imaginary Numbers
- **Definition**: Numbers involving the square root of negative values (involving √-1)
- **Data Science Use**: Encountered in advanced matrix decompositions (Chapter 4)
- **Recommendation**: For those interested, see "Imaginary Numbers are Real" YouTube playlist

**Practical Summary**: In data science, you'll primarily work with whole numbers, natural numbers, integers, real numbers, and occasionally rational numbers.

---

## 2. Order of Operations (PEMDAS)

### 2.1 The Hierarchy

Remember **PEMDAS**:
- **P**arentheses
- **E**xponents
- **M**ultiplication/Division (left to right)
- **A**ddition/Subtraction (left to right)

### 2.2 Example Expression

Consider: `2 × (3 + 2)² / 5 - 4`

**Step-by-step evaluation**:

1. **Parentheses**: (3 + 2) = 5
   - Expression becomes: `2 × 5² / 5 - 4`

2. **Exponents**: 5² = 25
   - Expression becomes: `2 × 25 / 5 - 4`

3. **Multiplication**: 2 × 25 = 50
   - Expression becomes: `50 / 5 - 4`

4. **Division**: 50 / 5 = 10
   - Expression becomes: `10 - 4`

5. **Subtraction**: 10 - 4 = 6
   - **Final Answer**: 6

### 2.3 Python Implementation

```python
# Example 1-1: Solving an expression in Python
my_value = 2 * (3 + 2)**2 / 5 - 4
print(my_value)  # prints 6.0
```

### 2.4 Best Practice: Use Extra Parentheses

```python
# Example 1-2: Clarity through parentheses
my_value = 2 * ((3 + 2)**2 / 5) - 4
print(my_value)  # prints 6.0
```

**Why This Matters**: 
- Provides clarity for yourself and others reading your code
- Establishes explicit control over evaluation order
- Prevents bugs when modifying expressions
- Serves as documentation of intent

---

## 3. Variables and Functions

### 3.1 What is a Variable?

- **Definition**: A named placeholder for an unspecified or unknown value
- **Mathematical Context**: Represents any real number (x, y, θ, β, etc.)
- **Python Implementation**: Simple assignment and operations

### 3.2 Example: User Input with Variables

```python
# Example 1-3: Variable operations with user input
x = int(input("Please input a number\n"))
product = 3 * x
print(product)
```

### 3.3 Greek Symbols in Data Science

Common variables and their meanings:

| Symbol | Name | Usage |
|--------|------|-------|
| θ | Theta | Angles, parameters |
| β | Beta | Regression coefficients |
| μ | Mu | Population mean |
| σ | Sigma | Standard deviation |
| λ | Lambda | Eigenvalues, decay rates |
| π | Pi | Mathematical constant |

**Python Note**: Greek symbols are awkward variable names; use descriptive names like `theta`, `beta`, `mu`, `sigma` instead.

### 3.4 Functions

- **Definition**: A mathematical relationship that maps inputs to outputs
- **Python Context**: Callable objects that transform inputs
- **Example**: f(x) = 2x + 3 in math becomes `def f(x): return 2*x + 3` in Python

### 3.5 Practical Tips

1. **Always use parentheses** in complex expressions for clarity
2. **Choose meaningful variable names** instead of Greek symbols when possible
3. **Document your variable meanings** in comments
4. **Test edge cases** with your mathematical functions

---

## 4. Exponents and Logarithms

### 4.1 Exponents

- **Definition**: Repeated multiplication (base^exponent)
- **Examples**:
  - 2³ = 2 × 2 × 2 = 8
  - x² represents x × x
- **In Data Science**: Used in polynomial features, growth models, and normalization

### 4.2 Logarithms

- **Definition**: The inverse of exponentiation (log_b(x) = y means b^y = x)
- **Natural Logarithm (ln or log)**: Base e = 2.718281828...
- **Applications**:
  - Modeling exponential growth/decay
  - Handling skewed data distributions
  - Normalizing features
- **Common Logarithm (log₁₀)**: Base 10

### 4.3 Python Implementation

```python
import math

# Exponents
result = 2 ** 3  # 8
x_squared = x ** 2

# Natural logarithm
ln_result = math.log(x)  # base e
log10_result = math.log10(x)  # base 10

# Log properties
math.log(a * b) == math.log(a) + math.log(b)
math.log(a / b) == math.log(a) - math.log(b)
math.log(a ** b) == b * math.log(a)
```

---

## 5. Derivatives

### 5.1 Concept

- **Definition**: The rate of change of a function at a point
- **Intuitive Understanding**: Slope of the tangent line to a curve
- **Applications**:
  - Optimization (finding maximum/minimum)
  - Gradient descent in machine learning
  - Understanding model sensitivity

### 5.2 Python with SymPy

```python
from sympy import symbols, diff

x = symbols('x')
f = x**2 + 3*x + 2

# First derivative
f_prime = diff(f, x)  # Returns: 2*x + 3

# Second derivative
f_double_prime = diff(f, x, 2)  # Returns: 2
```

### 5.3 Chain Rule

```python
# Composite function: f(g(x))
# If f(x) = sin(x²), then f'(x) = cos(x²) * 2x

from sympy import symbols, sin, diff

x = symbols('x')
g = x**2
f = sin(g)

f_prime = diff(f, x)  # Uses chain rule automatically
# Result: 2*x*cos(x**2)
```

### 5.4 Practical Use in Machine Learning

- **Gradient Descent**: Uses derivatives to update model parameters
- **Backpropagation**: Computes gradients through neural networks
- **Optimization**: Finds optimal hyperparameters

---

## 6. Integrals

### 6.1 Concept

- **Definition**: The accumulation of quantities (area under a curve)
- **Intuitive Understanding**: Summing infinitely many thin rectangles
- **Applications**:
  - Computing probabilities from PDFs
  - Expected values in statistics
  - Area calculations for decision boundaries

### 6.2 Python with SymPy

```python
from sympy import symbols, integrate

x = symbols('x')

# Definite integral from 0 to 1 of x²
result = integrate(x**2, (x, 0, 1))
# Result: 1/3

# Indefinite integral (antiderivative)
indefinite = integrate(x**2, x)
# Result: x³/3 + C (C is constant of integration)

# Double integral
definite_2d = integrate(integrate(x**2 + y**2, (x, 0, 1)), (y, 0, 1))
```

### 6.3 Numerical Integration

For functions that can't be integrated symbolically:

```python
from scipy import integrate

# Numerical integration of a complex function
f = lambda x: x**2 * math.sin(x)
result, error = integrate.quad(f, 0, math.pi)
print(f"Integral: {result}, Error estimate: {error}")
```

### 6.4 Practical Use in Machine Learning

- **Probability Density Functions**: Normalizing distributions
- **Expected Value**: Computing mean of random variables
- **Loss Functions**: Integrating over data distributions

---

## 7. Essential Python Libraries for Chapter 1

| Library | Purpose | Key Functions |
|--------|---------|---------------|
| `numpy` | Numerical operations | Arrays, broadcasting |
| `sympy` | Symbolic math | `diff()`, `integrate()`, `solve()` |
| `scipy` | Numerical analysis | `quad()`, optimization |
| `scipy.special` | Special functions | `gamma()`, `beta()` |
| `matplotlib` | Visualization | Plotting functions |

**Installation**:
```bash
pip install numpy sympy scipy matplotlib
```

---

## 8. Chapter Summary

### Key Concepts Reviewed

1. **Number Systems**: Natural, whole, integers, rational, irrational, real numbers
2. **Order of Operations**: PEMDAS hierarchy with Python examples
3. **Variables and Functions**: Mathematical notation in Python context
4. **Exponents and Logarithms**: Growth modeling, normalization
5. **Derivatives**: Rates of change, optimization
6. **Integrals**: Area under curves, probability calculations
7. **Python Implementation**: SymPy for symbolic math, SciPy for numerical

### Practical Takeaways

- You don't need to memorize all formulas; Python does the heavy lifting
- Understanding the math helps you:
  - Debug machine learning models
  - Choose appropriate algorithms
  - Interpret results correctly
  - Extend beyond library defaults

### Next Steps

This chapter has laid the groundwork. The remaining chapters will build on these foundations:
- **Chapter 2**: Python for Data Science
- **Chapter 3**: Linear Algebra
- **Chapter 4**: Matrix Decomposition
- **Chapter 5**: Probability
- **Chapter 6**: Statistics
- **Chapters 7-9**: Machine Learning applications

---

## References

- *No Bullshit Guide to Math and Physics* by Ivan Savov
- *Mathematics 1001* by Dr. Richard Elwes
- O'Reilly's Python resources for data science

---

## Exercises

1. **Order of Operations**: Create expressions and verify results in Python
2. **Variables**: Write functions that use different variable types
3. **Exponents/Logs**: Model exponential growth scenarios
4. **Derivatives**: Compute gradients for simple functions
5. **Integrals**: Calculate areas under curves using both symbolic and numerical methods

---

*Note: This summary covers the essential mathematical concepts from Chapter 1. As stated in the book, these concepts are "essential math" rather than comprehensive mathematical knowledge. The goal is practical understanding for data science applications.*