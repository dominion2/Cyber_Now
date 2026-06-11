# 🐍 Python for Data Science Roadmap: From Syntax to Insights

> 📚 **Purpose**: A comprehensive guide to mastering Python as the primary tool for Data Science, Machine Learning, and Automation.
> 
> 🎯 **Goal**: Build a path from basic programming logic to advanced data manipulation and model deployment.

---

## 📋 Table of Contents

1. [Python Fundamentals](#1-python-fundamentals)
2. [Data Structures: Lists, Dicts & Sets](#2-data-structures-lists-dicts--sets)
3. [Control Flow & Logic](#3-control-flow--logic)
4. [Functional Programming: Functions & Lambdas](#4-functional-programming-functions--lambdas)
5. [The 'Big Three' Libraries: NumPy, Pandas, Matplotlib](#5-the-big-three-libraries-numpy-pandas-matplotlib)
6. [Data Cleaning & Wrangling](#6-data-cleaning--wrangling)
7. [Exploratory Data Analysis (EDA)](#7-exploratory-data-analysis-eda)
8. [Automation & Scripting](#8-automation--scripting)
9. [Object-Oriented Programming (OOP) for ML](#9-object-oriented-programming-oop-for-ml)
10. [Next Steps & Projects](#10-next-steps--projects)
11. [Practical Applications](#11-practical-applications)

---

## 1. Python Fundamentals

### 1.1 Variables & Basic Math
```python
# Simple Assignment
x = 10
y = 3.5

# Math Operations (Easy to use in formulas)
total = x + y       # Addition
product = x * y     # Multiplication
squared = x ** 2    # Power of 2
remainder = 10 % 3  # Modulo (Returns 1)
```

### 1.2 Strings (Text Data)
```python
# Formatting text for outputs
name = "Jason"
print(f"Data analysis for {name}") # f-string (Best practice)

# Common String Methods
msg = "  python is fun  "
print(msg.strip().capitalize()) # "Python is fun"
```

---

## 2. Data Structures: Lists, Dicts & Sets

### 2.1 Lists (Managing Collections)
```python
data = [10, 20, 30]

# Add & Remove
data.append(40)     # [10, 20, 30, 40]
data.pop(0)         # Removes first item (10)

# Slicing (Crucial for datasets)
subset = data[1:3]  # Get items from index 1 to 2
```

### 2.2 Dictionaries (Records)
```python
# Storing multi-part data
record = {"id": 1, "status": "active"}

# Getting and Setting
record["status"] = "inactive"    # Update value
record["last_login"] = "12:00"   # Add new key
```

### 2.3 Sets (Unique Collections)
Useful for finding unique values in a dataset or removing duplicates.

---

## 3. Control Flow & Logic

Logic is the decision-making engine of your scripts. In Data Science, we use this to filter data or handle edge cases.

### 3.1 Conditional Statements (If/Else)
```python
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
else:
    print("Review needed")
```

### 3.2 Loops: Iterating Over Data
- **For Loops**: Best for iterating over a known sequence (like a list of rows).
- **While Loops**: Runs as long as a condition is true.

```python
# Iterating through a list
features = ["age", "income", "zip_code"]
for f in features:
    print(f"Processing feature: {f}")
```

---

## 4. Functional Programming: Functions & Lambdas

Functions allow you to reuse code, making your models and analysis repeatable.

### 4.1 Defining Functions
```python
def calculate_bmi(weight_kg, height_m):
    """Calculates Body Mass Index (BMI)."""
    return weight_kg / (height_m ** 2)

# Usage
my_bmi = calculate_bmi(70, 1.75)
```

### 4.2 Data Science Speed-Ups
- **List Comprehensions**: A concise way to create lists.
    ```python
    # Standard: [0, 1, 4, 9, 16]
    squares = [x**2 for x in range(5)]
    ```
- **Lambda Functions**: Anonymous, one-line functions used for quick data transformations.
    ```python
    # Double a value
    double = lambda x: x * 2
    ```

---

## 5. The 'Big Three' Libraries: Pandas, NumPy, Matplotlib

> 🌟 **The Golden Rule of Thumb**: Use SQL to clean, filter, and aggregate massive datasets down to a manageable size on the database server. Then, pull that refined dataset into pandas for deep-dive analysis, visualization, and machine learning.

### 5.1 Pandas: The Data Scientist's Spreadsheet
Pandas is used for data manipulation and analysis.

#### A. Pandas Series: The 1D Building Block
A **Series** is a labeled, one-dimensional array. It's like a single column in Excel or a list with custom labels.

```python
import pandas as pd

# 1. From a List (Default numeric index)
s = pd.Series([10, 20, 30])

# 2. From a Dictionary (Keys become labels)
data = {'Jan': 100, 'Feb': 200, 'Mar': 300}
s_sales = pd.Series(data)

# 3. Attributes (Inspecting the data)
print(s_sales.index)  # ['Jan', 'Feb', 'Mar']
print(s_sales.values) # [100, 200, 300]

# 4. Boolean Filtering (Fast subsets)
high_sales = s_sales[s_sales > 150] # Returns only Feb and Mar
```

#### B. DataFrames: The 2D Spreadsheet
The primary structure is the **DataFrame** (rows and columns).
```python
import pandas as pd

# 1. From a Dictionary (Keys = Columns)
data_dict = {
    "Frequency": [20, 50, 8],
    "Location": [2, 3, 1],
    "Type": ["Interneuron", "Interneuron", "Pyramidal"]
}
df = pd.DataFrame(data_dict, index=["C1", "C2", "C3"])

# 2. From a List of Lists (Requires explicit column names)
data_list = [[20, 2, "A"], [50, 3, "B"]]
df_list = pd.DataFrame(data_list, columns=["Freq", "Loc", "Label"])
```

#### B. Selecting & Modifying Data
```python
# Select a Column
freq_col = df["Frequency"]

# Select a Row (Must use .loc)
row_1 = df.loc["C1"]

# Rename Headers/Rows
df.columns = ["Freq (Hz)", "Loc (cm)", "Cell Type"]
df.index = ["Cell_1", "Cell_2", "Cell_3"]
```

#### C. Statistical Inspection
These methods automatically ignore non-numeric columns (like strings).
```python
df.mean()    # Average of columns
df.median()  # Middle value
df.std()     # Standard deviation

# Calculate across ROWS (per sample)
df.mean(axis=1)
```

#### D. Advanced Data Manipulation
These techniques allow you to clean, filter, and organize your data for analysis.

**1. Boolean Indexing (Multi-Condition Filtering)**:
Use `&` (AND) and `|` (OR). **Note**: Each condition must be in parentheses `()`.
```python
# Find rows where frequency > 20 AND type is 'Interneuron'
filtered_df = df[(df['Freq (Hz)'] > 20) & (df['Cell Type'] == 'Interneuron')]

# Find rows where frequency is 50 OR frequency is 8
subset_df = df[(df['Freq (Hz)'] == 50) | (df['Freq (Hz)'] == 8)]
```

**2. Sorting Values**:
Organize your data based on one or more columns.
```python
# Sort by Frequency (Ascending)
df_sorted = df.sort_values(by='Freq (Hz)')

# Sort by Type (Alphabetical) then Frequency (Descending)
df_multi_sort = df.sort_values(by=['Cell Type', 'Freq (Hz)'], ascending=[True, False])
```

**3. Grouping Data (Groupby)**:
Summarize data based on a category (e.g., finding the average frequency for each Cell Type).
```python
# Group by 'Cell Type' and find the mean of other columns
grouped_stats = df.groupby('Cell Type').mean()
```

**4. Handling Missing Data (NaN)**:
Crucial for real-world datasets which often have "holes."
```python
# Remove any rows with missing values
df_clean = df.dropna()

# Fill missing values with a specific number (like 0 or the mean)
df_filled = df.fillna(0)
```

#### E. Quick Math & Adding Columns
```python
# Element-wise math (Triples every value)
df_tripled = df * 3

# Adding a new derived column
df['Normalized'] = df['Freq (Hz)'] / df['Freq (Hz)'].mean()
```

### 5.2 NumPy: The Power of Arrays
NumPy (Numerical Python) is the fundamental package for scientific computing in Python. It provides a high-performance multidimensional array object (`ndarray`) and tools for working with these arrays.

#### A. Array Attributes & Characteristics
NumPy arrays are homogeneous (all elements must be of the same type). Dimensions are called **axes**, and the number of axes is the **rank**.

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.ndim)   # Number of dimensions (axes) -> 2
print(arr.shape)  # Dimensions of the array -> (2, 3)
print(arr.size)   # Total number of elements -> 6
print(arr.dtype)  # Data type of elements -> e.g., int64
```

#### B. Array Creation Techniques
Beyond basic lists, NumPy offers placeholders to avoid expensive "growing" of arrays.

```python
# From List/Tuple with explicit type
a = np.array([1, 2, 3], dtype='float')

# Placeholders
zeros = np.zeros((3, 4))        # 3x4 matrix of 0s
ones = np.ones((2, 2))          # 2x2 matrix of 1s
full = np.full((3, 3), 7)       # 3x3 matrix filled with 7s
empty = np.empty((2, 2))        # Uninitialized (values vary)

# Sequences
seq = np.arange(0, 30, 5)       # [0, 5, 10, 15, 20, 25] (step specified)
lin = np.linspace(0, 5, 10)     # 10 values between 0 and 5 (num elements specified)

# Random Data
rand_vals = np.random.random((2, 2)) # Random values [0.0, 1.0)
```

#### C. Reshaping & Flattening
You can change the shape of an array as long as the total number of elements remains the same.

```python
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) # (3, 4)

# Reshape to 3D: (2, 2, 3)
new_arr = arr.reshape(2, 2, 3)

# Flatten: Collapse into 1D
flat = arr.flatten() # [1, 2, 3, ..., 12]
```

#### D. Indexing & Slicing
NumPy supports advanced indexing for multi-dimensional data.

```python
arr = np.array([[-1, 2, 0, 4], [4, -0.5, 6, 0], [2.6, 0, 7, 8]])

# 1. Slicing: [rows, columns]
temp = arr[:2, ::2] # First 2 rows, every alternate column

# 2. Integer Indexing: Pass lists for each dimension
# Elements at (0,3), (1,2), (2,1)
picked = arr[[0, 1, 2], [3, 2, 1]]

# 3. Boolean Indexing: Filter by condition
filtered = arr[arr > 0]
```

#### E. Basic Operations (Element-wise & Unary)
NumPy operations are "vectorized," making them significantly faster than standard Python loops.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Binary Operators (Element-wise)
print(a + b)  # [5, 7, 9]
print(a * b)  # [4, 10, 18]
# matrix_prod = a.dot(b) # Dot product

# Unary Operators (ndarray methods)
arr = np.array([[1, 5, 6], [4, 7, 2]])
print(arr.max())            # Global max
print(arr.min(axis=0))      # Column-wise minimum
print(arr.sum(axis=1))      # Row-wise sum
print(arr.cumsum(axis=1))   # Cumulative sum along rows

# Universal Functions (ufunc)
np.sin(a)
np.exp(a)
np.sqrt(a)
```

#### F. Sorting Arrays
```python
arr = np.array([[1, 4, 2], [3, 4, 6], [0, -1, 5]])

# Simple sort (default axis is last axis)
sorted_all = np.sort(arr, axis=None) # Flattened sorted array
row_sort = np.sort(arr, axis=1)      # Each row sorted independently

# Structured Sorting (by field)
data = np.array([('Jason', 2009, 8.5), ('Alice', 2008, 8.7)],
                dtype=[('name', 'U10'), ('year', 'i4'), ('cgpa', 'f4')])
sorted_data = np.sort(data, order='year')
```

### 5.3 SciPy: Scientific Computing
SciPy builds on NumPy to provide advanced mathematical functions like optimization, integration, and statistics.

```python
from scipy import stats

# Normal Distribution
pdf_val = stats.norm.pdf(0) # Probability Density Function
cdf_val = stats.norm.cdf(0) # Cumulative Distribution Function (returns 0.5)

# T-Test (Comparing two groups)
t_stat, p_val = stats.ttest_ind(group_a, group_b)
```

---

## 📝 Learning Progress

- [x] Python Fundamentals (Syntax, Variables)
- [x] Data Structures (Lists, Dicts, Sets)
- [x] Control Flow & Logic
- [x] Functions & Modules
- [x] NumPy (Numerical Computing)
- [x] Pandas (Data Manipulation)
- [ ] Matplotlib/Seaborn (Visualization)
- [ ] Data Cleaning Projects

---

**Created**: 📅 2026-05-23
**Last Updated**: 📅 2026-06-11
**Version**: 1.2 (UMGC NumPy Tutorials Integrated)

---

## 11. Practical Applications

To see these Python concepts in action, check out the following project:
*   [**Temperature Data Wrangling & Classification**](./data-wrangling.md): Demonstrates the use of Python functions, loops, and conditional logic to perform unit conversion and feature engineering on raw sensor data.

---

> 🚀 **Keep Coding**: Python is a craft. The best way to learn is to write code every single day!
