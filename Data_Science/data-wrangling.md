# 🌡️ Temperature Data Wrangling & Classification

This project demonstrates foundational **Data Wrangling** and **Feature Engineering** techniques using a dataset of one week's worth of half-hourly temperature readings (336 data points).

## 🎯 Project Objectives
- **Data Transformation**: Perform unit conversion from Fahrenheit to Celsius using vectorized logic.
- **Categorical Feature Engineering**: Implement a custom classifier to bin continuous temperature data into qualitative categories (Freezing, Chilly, Pleasant, Warm).
- **Statistical Summarization**: Conduct frequency analysis to understand the distribution of temperature classes over the weekly period.

## 🛠️ The Data Wrangling Pipeline

### 1. The Raw Data
The dataset consists of 336 integers representing temperature values in Fahrenheit ($^\circ\text{F}$).

```python
# Initial data representing one week of half-hourly readings
tempData = [19, 21, 21, 21, 23, 23, 23, 21, 19, 21, 19, 21, 23, 27, 27, 28, 30, 30, 32, 32, 32, 32, 34, 34, ...]
```

### 2. Unit Conversion (F to C)
We apply the standard conversion formula to normalize the data for international scientific standards:
$$C = \frac{F - 32}{1.8}$$

```python
def fahrToCelsius(tempFahrenheit):
    """Converts Fahrenheit to Celsius."""
    convertedTemp = (tempFahrenheit - 32) / 1.8
    return convertedTemp
```

### 3. Classification (Feature Binning)
To make the data actionable for human-centric applications, we categorize the continuous Celsius values into four distinct classes based on thermal comfort levels:

| Class ID | Category | Criteria ($^\circ\text{C}$) |
| :--- | :--- | :--- |
| **0** | Freezing | $< -2$ |
| **1** | Chilly | $-2 \le \text{temp} \le 2$ |
| **2** | Pleasant | $2 < \text{temp} \le 15$ |
| **3** | Warm | $> 15$ |

```python
def tempClassifier(tempCelsius):
    """Categorizes temperature into qualitative bins."""
    if tempCelsius < -2:
        return 0
    elif tempCelsius <= 2:
        return 1
    elif tempCelsius <= 15:
        return 2
    else:
        return 3
```

## 📊 Results & Analysis

By iterating through the dataset and applying our transformation logic, we generated the following frequency distribution:

```python
# Processing the week's data
tempClasses = []
for tempF in tempData:
    tempC = fahrToCelsius(tempF)
    tempClass = tempClassifier(tempC)
    tempClasses.append(tempClass)

# Output Summary
# Class 0: (Freezing): 137 occurrences
# Class 1: (Chilly): 85 occurrences
# Class 2: (Pleasant): 114 occurrences
# Class 3: (Warm): 0 occurrences
```

### 🧠 Key Insight
The analysis reveals that this specific week was predominantly cold, with **~40%** of the time spent in the "Freezing" category and **0%** in the "Warm" category. This type of wrangling is essential for preparing raw sensor data for higher-level predictive modeling or climate reporting.


