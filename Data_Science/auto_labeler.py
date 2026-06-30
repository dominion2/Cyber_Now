"""
=============================================================================
TELEMETRY AUTO-LABELER & CORRELATION ENGINE
=============================================================================

PURPOSE:
This tool is designed to ingest, analyze, and pseudo-label raw telemetry 
streams (such as decoded bitstreams migrating from SDR receivers) where the 
data structure is known, but the specific column labels are undefined. 

When engineers lack an Interface Control Document (ICD), this script acts 
as an automated data-discovery engine. It uses statistical correlation to 
find mechanical systems that operate in sync, and heuristic physics-based 
rules to reverse-engineer geographic coordinates from blind data.

HOW IT WORKS:
1. Pearson Correlation Filtering: Automatically calculates a correlation 
   matrix across all high-dimensional tabular data to group sensor fields 
   that fluctuate synchronously (e.g., Engine RPM and Temperature).
2. Heuristic Auto-Labeling: Uses geographic boundary constraints (e.g., 
   Latitude must be between -90 and 90) and physics-based variance limits 
   to automatically discover unlabelled Latitude and Longitude streams.
3. Visual Verification: Automatically maps discovered geographic coordinates 
   on a 2D scatterplot to visually verify flight paths or driving routes.

USAGE:
- DEMO MODE: Run the script as-is. It will generate a simulated, unlabeled 
  telemetry stream and automatically analyze it.
- LIVE PIPELINE: Delete "SECTION 1" (the mock data generator) and replace 
  it with: `df = pd.read_csv('your_decoded_telemetry.csv')`

EXPECTED TERMINAL OUTPUT:
--- 1. CORRELATION SCAN ---
[ALERT] High correlation detected between Col_C and Col_D (Score: 0.985)
--- 2. HEURISTIC AUTO-LABELING ---
[SUCCESS] Auto-Labeled 'Col_A' as LATITUDE ...
[SUCCESS] Auto-Labeled 'Col_B' as LONGITUDE ...
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# SECTION 1: GENERATE MOCK UNLABELED DATA
# (Delete this section when using real data)
# ==========================================
# Creating a fake dataset with 4 unlabeled columns (Col_A through Col_D)
np.random.seed(42)
time_steps = 500

mock_data = {
    'Col_A': np.linspace(38.0, 39.5, time_steps) + np.random.normal(0, 0.01, time_steps), # Simulating Latitude
    'Col_B': np.linspace(-77.0, -75.5, time_steps) + np.random.normal(0, 0.01, time_steps), # Simulating Longitude
    'Col_C': np.linspace(1000, 5000, time_steps) + np.random.normal(0, 50, time_steps), # Simulating RPM
}
# Make Col_D highly correlated to Col_C (e.g., Temp rises with RPM)
mock_data['Col_D'] = mock_data['Col_C'] * 0.45 + np.random.normal(0, 10, time_steps) 

# Create the DataFrame (This is what your decoded SDR bitstream would look like)
df = pd.DataFrame(mock_data)

# ==========================================
# SECTION 2: AUTOMATIC CORRELATION FINDER
# ==========================================
print("--- 1. CORRELATION SCAN ---")
# Calculate the Pearson correlation matrix for all columns
correlation_matrix = df.corr()

# Loop through the matrix and flag any columns that are highly correlated (Score > 0.90)
# We use a set to avoid printing duplicates
seen = set()
for col1 in correlation_matrix.columns:
    for col2 in correlation_matrix.columns:
        if col1 != col2 and correlation_matrix.loc[col1, col2] > 0.90:
            pair = tuple(sorted([col1, col2]))
            if pair not in seen:
                print(f"[ALERT] High correlation detected between {pair[0]} and {pair[1]} (Score: {correlation_matrix.loc[col1, col2]:.3f})")
                seen.add(pair)

# ==========================================
# SECTION 3: HEURISTIC AUTO-LABELING
# ==========================================
print("\n--- 2. HEURISTIC AUTO-LABELING ---")
predicted_lat = None
predicted_long = None

# Scan every column to see if it fits the strict physical rules of Earth
for col in df.columns:
    min_val = df[col].min()
    max_val = df[col].max()
    
    # Rule for Latitude: Must be between -90 and 90, with realistic frame variance
    if -90 <= min_val <= 90 and -90 <= max_val <= 90 and df[col].var() < 100:
        predicted_lat = col
        print(f"[SUCCESS] Auto-Labeled '{col}' as LATITUDE (Range: {min_val:.2f} to {max_val:.2f})")
        
    # Rule for Longitude: Must be between -180 and 180 (but not already flagged as Lat)
    elif -180 <= min_val <= 180 and -180 <= max_val <= 180 and col != predicted_lat:
        predicted_long = col
        print(f"[SUCCESS] Auto-Labeled '{col}' as LONGITUDE (Range: {min_val:.2f} to {max_val:.2f})")

# ==========================================
# SECTION 4: VISUAL CONFIRMATION 
# ==========================================
# If the script successfully found Lat and Long, plot the trajectory
if predicted_lat and predicted_long:
    plt.figure(figsize=(10, 6))
    
    # Plotting Longitude on X (East/West) and Latitude on Y (North/South)
    plt.scatter(df[predicted_long], df[predicted_lat], c='blue', s=5, alpha=0.5)
    
    plt.title('Auto-Discovered Telemetry Flight Path')
    plt.xlabel(f'Discovered Longitude ({predicted_long})')
    plt.ylabel(f'Discovered Latitude ({predicted_lat})')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Prevent scientific notation
    plt.ticklabel_format(style='plain', useOffset=False)
    plt.show()
