# Chapter 2: Linear Algebra Fundamentals
## Essential Math for Data Science

---

## Overview

Linear algebra is the mathematical backbone of data science and machine learning. This chapter covers vector spaces, matrix operations, eigenvalues, eigenvectors, and their applications in practical data science scenarios.

---

## Core Concepts

### 1. Vectors and Vector Operations

**Definition**: A vector is an ordered collection of numbers that represents a point in space or a direction.

**Operations**:
- **Addition**: Component-wise addition
  ```
  [1, 2, 3] + [4, 5, 6] = [5, 7, 9]
  ```
- **Scalar Multiplication**: Multiply each component by a scalar
  ```
  2 × [1, 2, 3] = [2, 4, 6]
  ```
- **Dot Product**: Measures similarity between vectors
  ```
  [1, 2] • [3, 4] = 1×3 + 2×4 = 11
  ```
- **Norm (Magnitude)**: Length of a vector
  ```
  ||[3, 4]|| = √(3² + 4²) = √25 = 5
  ```

### 2. Matrices and Matrix Operations

**Definition**: A matrix is a 2D array of numbers representing linear transformations.

**Key Operations**:
- **Matrix Addition**: Element-wise addition
- **Matrix Multiplication**: Row × Column rule
  ```
  [1 2]   [3 4]   [7 14]
  [3 4] × [5 6] = [23 34]
  ```
- **Matrix Transpose**: Swap rows and columns
- **Matrix Inverse**: Reverse the transformation (when it exists)
- **Determinant**: Scalar value indicating invertibility

### 3. Eigenvalues and Eigenvectors

**Definition**: For matrix A, a pair (λ, v) satisfies:
  ```
  Av = λv
  ```
Where v is an eigenvector and λ is the eigenvalue.

**Applications**:
- Principal Component Analysis (PCA)
- Face recognition
- Google PageRank algorithm

### 4. Vector Spaces and Subspaces

**Key Concepts**:
- **Span**: All linear combinations of vectors
- **Basis**: Linearly independent set that spans a space
- **Dimension**: Number of vectors in a basis
- **Null Space**: Solutions to Ax = 0
- **Range/Column Space**: All possible outputs of Ax

### 5. Orthogonality and Projection

**Orthogonal Vectors**: Vectors perpendicular to each other (dot product = 0)

**Projection Formula**:
  ```
  proj_v(u) = (u • v / v • v) × v
  ```

**Applications**: Least squares regression, dimensionality reduction

### 6. Symmetric Matrices and Quadratic Forms

**Symmetric Matrices**: A = A^T (transpose equals itself)

**Properties**:
- All eigenvalues are real
- Eigenvectors are orthogonal
- Diagonalizable via orthogonal matrices

**Quadratic Forms**: x^T Ax where A is symmetric

### 7. Singular Value Decomposition (SVD)

**Decomposition**: A = UΣV^T

**Components**:
- **U**: Left singular vectors
- **Σ**: Diagonal matrix of singular values
- **V**: Right singular vectors

**Applications**:
- Image compression
- Latent semantic analysis
- Noise reduction

---

## Data Science Applications

### 1. Recommendation Systems
- **Matrix Factorization**: Decompose user-item matrices
- **Latent Factors**: Capture underlying patterns
- **Collaborative Filtering**: Predict missing ratings

### 2. Image Processing
- **Convolution**: Filter images using kernels
- **PCA**: Reduce image dimensions
- **Face Recognition**: Eigenfaces method

### 3. Natural Language Processing
- **TF-IDF Matrices**: Document-term representations
- **Word Embeddings**: Vectors representing words
- **Topic Modeling**: Latent Dirichlet Allocation (LDA)

### 4. Dimensionality Reduction
- **PCA**: Maximize variance in fewer dimensions
- **LDA**: Supervised dimensionality reduction
- **t-SNE/UMAP**: Non-linear dimensionality reduction

---

## Python Implementation

### Basic Operations with NumPy

```python
import numpy as np

# Create vectors
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# Operations
sum_v = v1 + v2
dot_product = np.dot(v1, v2)
norm = np.linalg.norm(v1)

# Create matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix operations
C = A @ B  # Matrix multiplication
AT = A.T   # Transpose
det = np.linalg.det(A)
inv = np.linalg.inv(A)
eigvals, eigvecs = np.linalg.eig(A)
```

### Eigen Decomposition

```python
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")
```

### SVD Example

```python
U, S, Vt = np.linalg.svd(A)
print(f"Singular values: {S}")
print(f"U shape: {U.shape}")
print(f"Vt shape: {Vt.shape}")
```

### PCA Implementation

```python
from sklearn.decomposition import PCA

# Standardize data
X_centered = X - X.mean(axis=0)

# Perform PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_centered)

# Explained variance
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
```

### Matrix Factorization (Recommendation)

```python
from sklearn.svd import TruncatedSVD

# Factorize user-item matrix
svd = TruncatedSVD(n_components=50)
U, S, Vt = svd.fit_transform(user_item_matrix)

# Reconstruct
reconstructed = U @ Vt
```

---

## Key Takeaways

1. **Linear Algebra is Everywhere**: Almost every ML algorithm uses linear algebra internally.

2. **Matrix Operations are Optimized**: Libraries like NumPy use BLAS/LAPACK for speed.

3. **Understanding vs Using**: Know the math to debug and improve algorithms.

4. **Large-Scale Computations**: SVD and eigen decomposition handle massive datasets efficiently.

5. **Geometric Intuition**: Visualize transformations to understand algorithms better.

---

## Common Pitfalls

- **Singular Matrices**: Cannot invert (det = 0)
- **Numerical Stability**: Watch for floating-point errors
- **Memory Issues**: Large matrices need sparse representations
- **Condition Number**: Poor conditioning affects accuracy

---

## Essential Libraries

- **NumPy**: Core array operations
- **SciPy**: Linear algebra functions
- **scikit-learn**: PCA, SVD implementations
- **PyTorch/TensorFlow**: Deep learning tensors
- **SymPy**: Symbolic linear algebra

---

## Next Steps

- Practice matrix operations with real datasets
- Implement PCA from scratch
- Study applications in specific domains (images, text, etc.)
- Explore deep learning frameworks' linear algebra usage

---

*Note: This chapter typically appears after Chapter 1 (Basic Math and Calculus Review) and precedes more advanced topics like optimization and deep learning.*
