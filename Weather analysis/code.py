import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/Users/ADMIN/Documents/Data analysis project/Weather analysis/dataset/Weather_Dataset.csv')

#      INITIAL DATA ANALYSIS
#print(df.head())
#print(df.isnull().sum())
#print(df.isna().sum())

df['Date & Time'] = df['Date/Time'].apply(pd.to_datetime)

average_temp = df.describe().loc['mean','Temp_C']

def extract_month(date_time):
    import datetime as dt
    month = dt.datetime.strptime(str(date_time),'%Y-%m-%d %X')
    return month.strftime('%b')

def extract_day(date_time):
    import datetime as dt
    month = dt.datetime.strptime(str(date_time),'%Y-%m-%d %X')
    return month.strftime('%d')

if 'Months' not in df.columns.to_list():
    df['Months'] = df['Date & Time'].apply(extract_month)
    
if 'Date' not in df.columns.to_list():
    df['Date'] = df['Date & Time'].apply(extract_day)



min_range = df.loc[
    (df['Wind Speed_km/h'] != 0),
    ['Wind Speed_km/h']
    ].values[0][0]
max_range = df['Wind Speed_km/h'].max()

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# 1st plot
axs[0, 0].set_title('Humidity changes over months')
axs[0, 0].plot(df['Months'], df['Rel Hum_%'], color='red')

# 2nd plot
axs[0, 1].set_title('Highest temp in months')
axs[0, 1].plot(df['Months'], df['Temp_C'], color='yellow')

# 3rd plot
axs[1, 0].set_title('Speed range of wind')
axs[1, 0].bar(x=['Min Range', 'Max Range'], height=[min_range, max_range])


fig.suptitle('Weather Data Analysis')
plt.tight_layout()
plt.show()













