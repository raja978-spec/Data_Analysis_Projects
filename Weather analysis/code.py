import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/Users/ADMIN/Documents/Data analysis project/Weather analysis/dataset/Weather_Dataset.csv')

#      INITIAL DATA ANALYSIS
#print(df.info())
#print(df.isnull().sum())
#print(df.isna().sum())

df['Date & Time'] = df['Date/Time'].apply(pd.to_datetime)

average_temp = df.describe().loc['mean','Temp_C']

def extract_month(date_time):
    import datetime as dt
    month = dt.datetime.strptime(str(date_time),'%Y-%m-%d %X')
    return month.strftime('%b')

if 'Months' not in df.columns.to_list():
    df['Months'] = df['Date & Time'].apply(extract_month)

#all_months = df['Months'].unique().tolist()
print(df['Months'].shape, df['Temp_C'].shape)
plt.plot(df['Months'].tolist(), df['Temp_C'].tolist(), color='yellow')
plt.show()