import pandas as pd
import numpy as np

# -------------------------
# 1. Load the dataset
# -------------------------
df = pd.read_csv('Weather analysis\dataset\Weather_Dataset.csv')

# Convert 'Date' column to datetime format.
df['Date'] = pd.to_datetime(df['Date'])

# For time-based analyses, extract Month and Year.
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Create a Season column.
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'
    
df['Season'] = df['Month'].apply(get_season)

# -------------------------
# Q1. What is the average temperature across all days in the dataset?
# -------------------------
avg_temp = df['Temperature'].mean()

# -------------------------
# Q2. Which month has the highest average temperature?
# -------------------------
monthly_avg_temp = df.groupby('Month')['Temperature'].mean()
month_highest_avg = monthly_avg_temp.idxmax()

# -------------------------
# Q3. How does humidity vary across different seasons or months?
# -------------------------
monthly_avg_humidity = df.groupby('Month')['Humidity'].mean()
seasonal_avg_humidity = df.groupby('Season')['Humidity'].mean()

# -------------------------
# Q4. What is the range of wind speed observed in the dataset?
# -------------------------
wind_speed_min = df['WindSpeed'].min()
wind_speed_max = df['WindSpeed'].max()

# -------------------------
# Q5. Are there any missing or anomalous values in the dataset?
# -------------------------
# Checking for missing values:
missing_values = df.isna().sum()

# For anomalies, we can flag temperature values beyond 3 standard deviations.
temp_std = df['Temperature'].std()
temp_mean = df['Temperature'].mean()
zscore_temp = (df['Temperature'] - temp_mean) / temp_std
anomalies_temp = df[abs(zscore_temp) > 3]

# -------------------------
# Q6. What is the trend of temperature over time (daily, monthly, yearly)?
# -------------------------
# Set Date as the index and resample to monthly averages.
df_time = df.copy().set_index('Date')
temperature_trend = df_time['Temperature'].resample('M').mean()

# -------------------------
# Q7. Is there a noticeable pattern in precipitation or rainfall across different months?
# -------------------------
precipitation_monthly = df_time['Precipitation'].resample('M').sum()

# -------------------------
# Q8. How do temperature and humidity fluctuate daily or seasonally?
# -------------------------
# Assuming multiple records per day, we can compute daily min/max differences.
daily_stats = df_time.resample('D').agg({'Temperature': ['min', 'max'], 'Humidity': ['min', 'max']})
daily_stats['Temp_Fluctuation'] = daily_stats[('Temperature','max')] - daily_stats[('Temperature','min')]
daily_stats['Humidity_Fluctuation'] = daily_stats[('Humidity','max')] - daily_stats[('Humidity','min')]

# -------------------------
# Q9. Which time of year experiences the most extreme weather conditions (e.g., hottest, coldest, windiest days)?
# -------------------------
# Identify days with extreme conditions:
extreme_temp_high = df_time['Temperature'].idxmax()
extreme_temp_low = df_time['Temperature'].idxmin()
extreme_wind = df_time['WindSpeed'].idxmax()

# -------------------------
# Q10. Is there a correlation between temperature and humidity?
# -------------------------
correlation_temp_humidity = df['Temperature'].corr(df['Humidity'])

# -------------------------
# Q11. Does higher wind speed usually correspond to lower or higher temperatures?
# -------------------------
correlation_wind_temp = df['WindSpeed'].corr(df['Temperature'])

# -------------------------
# Q12. How does cloud cover relate to temperature and precipitation?
# -------------------------
# Check if CloudCover exists:
if 'CloudCover' in df.columns:
    correlation_cloud_temp = df['CloudCover'].corr(df['Temperature'])
    correlation_cloud_precip = df['CloudCover'].corr(df['Precipitation'])
else:
    correlation_cloud_temp = None
    correlation_cloud_precip = None

# -------------------------
# Q13. What are the top 10 hottest and coldest days in the dataset?
# -------------------------
hottest_days = df_time.nlargest(10, 'Temperature')
coldest_days = df_time.nsmallest(10, 'Temperature')

# -------------------------
# Q14. On which days did it rain or snow the most? (Assuming 'Precipitation' column captures this info.)
# -------------------------
max_precipitation_days = df_time.nlargest(10, 'Precipitation')

# -------------------------
# Q15. How frequently do extreme weather events (like high wind or high rainfall) occur?
# -------------------------
# Define extreme events as values above the 95th percentile.
extreme_wind_events = df_time[df_time['WindSpeed'] > df_time['WindSpeed'].quantile(0.95)]
extreme_precip_events = df_time[df_time['Precipitation'] > df_time['Precipitation'].quantile(0.95)]

# -------------------------
# Print out the results for each analysis question:
# -------------------------
print("Q1: Average Temperature:", avg_temp)
print("\nQ2: Month with Highest Average Temperature:", month_highest_avg)
print("\nQ3: Average Humidity by Month:")
print(monthly_avg_humidity)
print("\nQ3: Average Humidity by Season:")
print(seasonal_avg_humidity)
print("\nQ4: Wind Speed Range: Min =", wind_speed_min, ", Max =", wind_speed_max)
print("\nQ5: Missing Values in Each Column:")
print(missing_values)
print("\nQ5: Temperature Anomalies (Values beyond 3 standard deviations):")
print(anomalies_temp[['Temperature']])
print("\nQ6: Temperature Trend (Monthly Average):")
print(temperature_trend)
print("\nQ7: Monthly Total Precipitation:")
print(precipitation_monthly)
print("\nQ8: Daily Temperature and Humidity Fluctuations:")
print(daily_stats[['Temp_Fluctuation', 'Humidity_Fluctuation']].head())
print("\nQ9: Extreme Weather Days:")
print("   Highest Temperature Day:", extreme_temp_high)
print("   Lowest Temperature Day:", extreme_temp_low)
print("   Highest Wind Speed Day:", extreme_wind)
print("\nQ10: Correlation between Temperature and Humidity:", correlation_temp_humidity)
print("\nQ11: Correlation between Wind Speed and Temperature:", correlation_wind_temp)
if correlation_cloud_temp is not None:
    print("\nQ12: Correlation between Cloud Cover and Temperature:", correlation_cloud_temp)
    print("Q12: Correlation between Cloud Cover and Precipitation:", correlation_cloud_precip)
else:
    print("\nQ12: Cloud Cover column not available in the dataset.")
print("\nQ13: Top 10 Hottest Days:")
print(hottest_days[['Temperature']])
print("\nQ13: Top 10 Coldest Days:")
print(coldest_days[['Temperature']])
print("\nQ14: Top 10 Days with Highest Precipitation:")
print(max_precipitation_days[['Precipitation']])
print("\nQ15: Frequency of Extreme Weather Events:")
print("   Extreme Wind Events (above 95th percentile):", len(extreme_wind_events))
print("   Extreme Precipitation Events (above 95th percentile):", len(extreme_precip_events))
