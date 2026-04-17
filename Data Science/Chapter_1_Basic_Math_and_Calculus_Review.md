# Chapter 1: Basic Math and Calculus Review

**Essential Math for Data Science** by Thomas Nield
*O'Reilly Media, 2022*

---

## Overview

This chapter provides a comprehensive review of fundamental mathematical concepts essential for data science. It covers calculus, number theory, probability, statistics, linear algebra, and their practical applications in machine learning.

---

## 1. Calculus Fundamentals

### 1.1 Limits

**Concept**: Limits describe the behavior of a function as the input approaches a certain value.

**Definition**:
```
lim(x→c) f(x) = L
```
As x approaches c, f(x) approaches L.

**Applications in Data Science**:
- Defining continuity of loss functions
- Understanding asymptotic behavior of models
- Numerical stability analysis

### 1.2 Derivatives

**Concept**: Derivatives measure the rate of change of a function.

**Definition**:
```
f'(x) = lim(h→0) [f(x+h) - f(x)] / h
```

**Key Rules**:
- **Power Rule**: d/dx(x^n) = n·x^(n-1)
- **Chain Rule**: d/dx[f(g(x))] = f'(g(x))·g'(x)
- **Product Rule**: d/dx[f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)

**Python Implementation**:
```python
import sympy as sp

x = sp.symbols('x')
f = x**2 + 3*x + 2
f_prime = sp.diff(f, x)  # Returns 2*x + 3
```

**Applications**:
- Gradient descent optimization
- Finding maxima/minima of loss functions
- Sensitivity analysis

### 1.3 Integrals

**Concept**: Integrals calculate the accumulation of quantities and areas under curves.

**Definition**:
```
∫f(x) dx = F(x) + C  (where F'(x) = f(x))
```

**Applications in Data Science**:
- Computing probabilities from PDFs
- Calculating expected values
- Numerical integration for complex functions

---

## 2. Number Theory and Exponents

### 2.1 Euler's Number (e)

**Definition**: e ≈ 2.71828... (base of natural logarithms)

**Key Properties**:
- e^x is its own derivative
- Used in exponential growth/decay models
- Fundamental to continuous compounding

### 2.2 Logarithms

**Definition**: log_b(x) is the power to which b must be raised to obtain x.

**Key Properties**:
- log_b(xy) = log_b(x) + log_b(y)
- log_b(x^y) = y·log_b(x)
- ln(x) = log_e(x) (natural logarithm)

**Applications**:
- Linearizing exponential relationships
- Feature scaling (log transforms)
- Information theory (entropy calculations)

### 2.3 Continuous Compounding

**Formula**: A = P·e^(rt)

Where:
- A = final amount
- P = principal amount
- r = interest rate
- t = time

---

## 3. Probability Fundamentals

### 3.1 Bayes' Theorem

**Formula**:
```
P(A|B) = P(B|A)·P(A) / P(B)
```

**Interpretation**: Updates prior probability P(A) to posterior P(A|B) given evidence B.

**Applications in Data Science**:
- Spam filtering
- Medical diagnosis
- A/B testing

### 3.2 Binomial Distribution

**Formula**:
```
P(X=k) = C(n,k)·p^k·(1-p)^(n-k)
```

Where:
- C(n,k) = n! / (k!(n-k)!)
- p = probability of success
- n = number of trials
- k = number of successes

**Applications**:
- Binary classification models
- Success/failure experiments

### 3.3 Beta Distribution

**Purpose**: Conjugate prior for binomial distribution

**Formula**:
```
f(x|α,β) = x^(α-1)·(1-x)^(β-1) / B(α,β)
```

Where B(α,β) is the beta function.

---

## 4. Statistical Measures

### 4.1 Measures of Central Tendency

**Mean (Expected Value)**:
```
E[X] = Σ(x_i·p_i)  (for discrete variables)
E[X] = ∫x·f(x)dx  (for continuous variables)
```

**Median**: Middle value when data is sorted.

**Mode**: Most frequent value.

### 4.2 Variance and Standard Deviation

**Population Variance**:
```
σ² = Σ(x_i - μ)² / N
```

**Sample Variance**:
```
s² = Σ(x_i - x̄)² / (n-1)
```

**Standard Deviation**:
```
σ = √σ²
s = √s²
```

**Applications**:
- Risk assessment
- Feature scaling
- Outlier detection

### 4.3 Weighted Statistics

**Weighted Mean**:
```
x̄ = Σ(w_i·x_i) / Σw_i
```

Where w_i are weights (frequencies, probabilities).

---

## 5. Probability Distributions

### 5.1 Normal Distribution (Gaussian)

**Probability Density Function (PDF)**:
```
f(x) = (1 / (σ√(2π))) · e^(-(x-μ)² / (2σ²))
```

**Properties**:
- Mean (μ) determines location
- Standard deviation (σ) determines spread
- 68-95-99.7 rule (within 1, 2, 3 standard deviations)

**Cumulative Distribution Function (CDF)**:
```
F(x) = P(X ≤ x) = ∫(-∞ to x) f(t) dt
```

**Inverse CDF (Percentiles)**:
```
F⁻¹(p) = value where P(X ≤ value) = p
```

**Python Implementation**:
```python
from scipy.stats import norm

# Calculate PDF
pdf_value = norm.pdf(x, loc=0, scale=1)

# Calculate CDF
cdf_value = norm.cdf(x, loc=0, scale=1)

# Calculate inverse CDF (percentile)
percentile = norm.ppf(0.95, loc=0, scale=1)  # 95th percentile
```

### 5.2 Standard Normal Distribution

**Z-Score**:
```
Z = (x - μ) / σ
```

**Applications**:
- Hypothesis testing
- Confidence intervals
- Standardization of features

### 5.3 Central Limit Theorem

**Statement**: The sampling distribution of the sample mean approaches normal distribution as sample size increases, regardless of the population distribution.

**Implications**:
- Justifies use of normal distribution in statistical inference
- Foundation for many hypothesis tests

---

## 6. Linear Algebra Fundamentals

### 6.1 Vectors and Matrices

**Vector**: Ordered collection of numbers.

**Matrix**: 2D array of numbers.

**Operations**:
- Addition, subtraction, scalar multiplication
- Matrix multiplication
- Transpose
- Dot product

### 6.2 Determinants

**Definition**: Scalar value representing the scaling factor of a linear transformation.

**Properties**:
- det(A) = 0 means A is singular (no inverse)
- det(AB) = det(A)·det(B)

### 6.3 Eigenvalues and Eigenvectors

**Definition**: For matrix A, eigenvector v satisfies:
```
A·v = λ·v
```
Where λ is the eigenvalue.

**Applications**:
- Principal Component Analysis (PCA)
- Face recognition
- Solving differential equations

### 6.4 Matrix Inverse

**Definition**: Matrix A⁻¹ such that A·A⁻¹ = I (identity matrix).

**Condition**: Exists only if det(A) ≠ 0.

**Python Implementation**:
```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
A_inv = np.linalg.inv(A)
```

---

## 7. Combinatorics

### 7.1 Permutations

**Formula**:
```
P(n,r) = n! / (n-r)!
```

Where n! = n·(n-1)·...·1

**Applications**: Order matters (password combinations, race rankings)

### 7.2 Combinations

**Formula**:
```
C(n,r) = n! / (r!(n-r)!)
```

**Applications**: Order doesn't matter (hand cards, committee selection)

### 7.3 Probability Rules

**Addition Rule**: P(A∪B) = P(A) + P(B) - P(A∩B)

**Multiplication Rule**: P(A∩B) = P(A)·P(B|A)

---

## 8. Machine Learning Applications

### 8.1 Linear Regression

**Model**: y = Xβ + ε

**Ordinary Least Squares**:
```
β̂ = (X^T·X)⁻¹·X^T·y
```

### 8.2 Logistic Regression

**Model**: P(y=1|x) = 1 / (1 + e^(-β₀ - β₁x))

**Applications**: Binary classification

### 8.3 k-Nearest Neighbors (k-NN)

**Concept**: Classify based on majority vote of k nearest training points.

### 8.4 Support Vector Machines (SVM)

**Objective**: Find hyperplane maximizing margin between classes.

**Kernel Trick**: Maps data to higher dimensions for non-linear separation.

### 8.5 Naive Bayes

**Based on**: Bayes' theorem with feature independence assumption.

**Applications**: Text classification, spam filtering.

### 8.6 Decision Trees

**Structure**: Tree-based model making decisions via binary splits.

### 8.7 Random Forests

**Concept**: Ensemble of decision trees trained on bootstrap samples.

### 8.8 Gradient Boosting

**Concept**: Sequential model where each corrects errors of previous models.

---

## 9. Essential Python Libraries

### Core Libraries

| Library | Purpose | Key Functions |
|---------|---------|---------------|
| `numpy` | Numerical operations | `np.array()`, `np.mean()`, `np.linalg.inv()` |
| `scipy` | Scientific computing | `scipy.stats.norm()`, `scipy.integrate()` |
| `sympy` | Symbolic math | `sp.diff()`, `sp.integrate()` |
| `scikit-learn` | ML models | `LinearRegression()`, `RandomForest()` |
| `matplotlib` | Visualization | `plt.plot()`, `plt.scatter()` |
| `pandas` | Data manipulation | `pd.read_csv()`, `DataFrame` |

### Installation

```bash
pip install numpy scipy sympy scikit-learn matplotlib pandas
```

---

## 10. Best Practices and Tips

1. **Understand the math**: Don't just call libraries; understand what they compute.

2. **Validate assumptions**: Check data distributions before applying algorithms.

3. **Handle edge cases**: Be aware of division by zero, singular matrices, etc.

4. **Use vectorization**: Prefer numpy operations over Python loops.

5. **Document your code**: Mathematical formulas are not self-documenting.

6. **Test incrementally**: Verify each mathematical operation separately.

7. **Choose appropriate libraries**: Not all libraries are equal in performance.

8. **Monitor numerical stability**: Watch for overflow/underflow issues.

9. **Visualize**: Graphs help identify issues and verify results.

10. **Continuous learning**: Math evolves; stay updated.

---

## Summary

Chapter 1 establishes the mathematical foundation for all subsequent chapters in "Essential Math for Data Science." Key takeaways include:

- **Calculus** enables optimization and understanding model behavior
- **Probability** provides the framework for inference and uncertainty quantification
- **Linear algebra** is essential for understanding ML algorithms
- **Statistics** forms the basis for model evaluation and selection
- **Python libraries** implement these concepts efficiently

Understanding these fundamentals allows data scientists to:
- Debug model failures
- Design better experiments
- Interpret model outputs
- Make informed architectural decisions

---

## Next Steps

Proceed to **Chapter 2** where we explore:
- More advanced calculus applications
- Statistical learning theory
- Additional ML algorithm analysis

---

*Generated from "Essential Math for Data Science" - Thomas Nield (2022)*