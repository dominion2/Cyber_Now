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

### 3. Preprocessing for Machine Learning (Scikit-Learn Prep)
Pandas is the bridge between raw data and machine learning models. The image `pandas_machine_learning.png` outlines critical preprocessing steps:

- **Feature Selection**: Selecting the most predictive columns.
- **Feature Scaling**: Normalizing or standardizing numerical data so all features have a similar influence.
- **Encoding Categorical Data**: Converting text labels into numeric values using techniques like **One-Hot Encoding** (`pd.get_dummies()`).
- **Data Splitting**: Separating your dataset into Features ($X$) and Target Labels ($y$).

```python
# 1. Feature/Target Separation
X = df.drop('Target_Column', axis=1) # All features except the answer
y = df['Target_Column']              # The answer we want to predict

# 2. Categorical Encoding (One-Hot)
# Converts 'Cell Type' into binary columns (Interneuron_1, Pyramidal_1, etc.)
X = pd.get_dummies(X, columns=['Cell Type'])

# 3. Training/Test Split (Handled by scikit-learn but uses Pandas objects)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

### 4. Time-Series Analysis (Temporal Wrangling)
Often, data includes timestamps that require special handling. The image `pandas_time.png` highlights essential Pandas tools for time-centric datasets:

- **Datetime Conversion**: Converting strings to objects using `pd.to_datetime()`.
- **DatetimeIndex**: Setting time as the index for powerful slicing (e.g., `df['2017-06']`).
- **Resampling**: Aggregating data into different frequencies (e.g., converting hourly data to daily means).
- **Rolling Windows**: Calculating moving statistics (like a 7-day moving average) to smooth out noise.

```python
# 1. Convert column to datetime objects
df['YR--MODAHRMN'] = pd.to_datetime(df['YR--MODAHRMN'], format='%Y%m%d%H%M')

# 2. Set as index for time-based slicing
df.set_index('YR--MODAHRMN', inplace=True)

# 3. Resampling: Get Daily Mean Temperature
daily_temp = df['Celsius'].resample('D').mean()

# 4. Rolling Window: 7-period moving average
smooth_temp = df['Celsius'].rolling(window=7).mean()
```

### 5. Advanced Data Manipulation (Complex Wrangling)
To handle complex data engineering tasks, the image `advanced_pandas.png` introduces high-level transformation techniques:

- **Merging & Joining**: Combining multiple DataFrames into a single source of truth using shared keys (`pd.merge()`).
- **Pivot Tables**: Reshaping data from "long" to "wide" format to summarize relationships between multiple variables (`df.pivot_table()`).
- **Multi-Indexing**: Creating hierarchical indexes to organize data across multiple dimensions (e.g., Year > Month > Station).
- **Concatenation**: Stack datasets vertically or horizontally using `pd.concat()`.

```python
# 1. Merge: Combine station metadata with temperature logs
merged_df = pd.merge(df, station_info, on='USAF', how='inner')

# 2. Pivot Table: Average Temperature by Month and Station
pivot = df.pivot_table(values='Celsius', index='Month', columns='Station', aggfunc='mean')

# 3. Concatenation: Stacking data from different years
full_dataset = pd.concat([df_2016, df_2017], axis=0)

# 4. Multi-Indexing: Group by multiple levels
grouped = df.groupby(['Station', 'Month'])['Celsius'].agg(['mean', 'std'])
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


