# 🌡️ Temperature Data Wrangling & Classification

This guide demonstrates foundational and advanced **Data Wrangling** and **Feature Engineering** techniques, moving from raw Python logic to professional-grade **Pandas** and **NumPy** workflows.

## 🎯 Objectives
- **Data Transformation**: Perform unit conversion and normalization.
- **Selective Loading**: Efficiently import specific datasets using `usecols`.
- **Handling Messy Data**: Identify and clean custom missing data indicators (`*`, `**`, etc.).
- **Feature Engineering**: Implement binning and classification for categorical analysis.
- **Vectorized Analysis**: Use high-performance library methods for statistical summaries.

---

## 🛠️ The Data Wrangling Pipeline

### 1. Efficient Data Loading (Pandas)
In professional workflows, we often deal with large datasets (like the NOAA meteorological data). Instead of loading the entire file, we select only what we need and define what "null" looks like.

```python
import pandas as pd

# Define custom NA values found in raw sensor data
na_indicators = ['*', '**', '***', '****', '*****', '******']

# Selective import: Only load the columns we need for analysis
chosen = pd.read_csv(
    '6153237444115dat.csv',
    usecols=['USAF', 'YR--MODAHRMN', 'TEMP', 'MAX', 'MIN'],
    na_values=na_indicators
)

# Clean rows where primary feature (TEMP) is missing
df = chosen.dropna(subset=['TEMP']).copy()
```

### 2. Unit Conversion (Vectorized vs. Functional)
We normalize Fahrenheit ($^\circ\text{F}$) to Celsius ($^\circ\text{C}$) for international scientific standards:
$$C = \frac{F - 32}{1.8}$$

While we can use a standard function, **Pandas/NumPy** allow for vectorized math which is significantly faster:

```python
# Functional approach (Used in data_exploration.py)
def fahrToCelsius(tempF):
    return (tempF - 32) / 1.8

# Application: Iterative vs Vectorized
# Iterative (for loop)
selected['Celsius'] = [round(fahrToCelsius(f), 1) for f in selected['TEMP']]

# Vectorized (Standard Practice)
selected['Celsius'] = ((selected['TEMP'] - 32) / 1.8).round(1)
```

### 3. Classification (Feature Binning)
To make data actionable, we categorize continuous values into thermal comfort bins:

| Class ID | Category | Criteria ($^\circ\text{C}$) |
| :--- | :--- | :--- |
| **0** | Freezing | $< -2$ |
| **1** | Chilly | $-2 \le \text{temp} \le 2$ |
| **2** | Pleasant | $2 < \text{temp} \le 15$ |
| **3** | Warm | $> 15$ |

**Implementation Example:**
```python
def tempClassifier(tempCelsius):
    if tempCelsius < -2: return 0
    elif tempCelsius <= 2: return 1
    elif tempCelsius <= 15: return 2
    else: return 3

# Adding the categorical feature
selected['Category'] = selected['Celsius'].apply(tempClassifier)
```

---

## 📊 Results & Analysis

### Descriptive Statistics by Station
Once wrangled, we can compare metrics across different locations (e.g., Helsinki vs. Rovaniemi) effortlessly.

```python
# Isolating specific stations (Helsinki=29980, Rovaniemi=28450)
kumpula = selected[selected['USAF'] == 29980]
rovaniemi = selected[selected['USAF'] == 28450]

# Monthly Summary (May/June 2017)
print(f"Kumpula Median: {kumpula['Celsius'].median()}°C")
print(f"Rovaniemi Median: {rovaniemi['Celsius'].median()}°C")
```

### 🧠 Key Insights
Professional data wrangling isn't just about cleaning; it's about **optimization**. Using `na_values` during import and vectorized math for transformations reduces the lines of code and increases performance, especially when scaling from a week's worth of data to several years of meteorological records.

---
**Reference Project**: [data_exploration.py](./data_exploration.py)


