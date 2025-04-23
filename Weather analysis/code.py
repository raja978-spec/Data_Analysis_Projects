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

# fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# # 1st plot
# axs[0, 0].set_title('Humidity changes over months')
# axs[0, 0].plot(df['Months'], df['Rel Hum_%'], color='red')

# # 2nd plot
# axs[0, 1].set_title('Highest temp in months')
# axs[0, 1].plot(df['Months'], df['Temp_C'], color='yellow')

# # 3rd plot
# axs[1, 0].set_title('Speed range of wind')
# axs[1, 0].bar(x=['Min Range', 'Max Range'], height=[min_range, max_range])

# fig.suptitle('Weather Data Analysis')
# plt.tight_layout(pad=2.0)
# #plt.show()

def z_score_for_anomly_detection(column):
    m = df[column].mean()
    sd = df[column].std()
    z_scores = abs(df[column] - m) / sd
    anomalies = df[z_scores > 3]
    if len(anomalies) != 0:
        print(f"{column} has anomaly values:\n", anomalies[[column]])

    
for i in ['Temp_C','Dew Point Temp_C','Rel Hum_%','Wind Speed_km/h','Visibility_km']:
    #z_score_for_anomly_detection(i)
    pass
'''
OUPUT:

Wind Speed_km/h has anomaly values:
       Wind Speed_km/h
33                 44
34                 43
36                 48
409                83
410                70
              ...
8538               46
8669               43
8671               44
8677               48
8678               46
'''

#
def extract_year(date_time):
    import datetime as dt
    month = dt.datetime.strptime(str(date_time),'%Y-%m-%d %X')
    return month.strftime('%Y')
if 'Year' not in df.columns.to_list():
    df['Year'] = df['Date & Time'].apply(extract_year)

# print(df['Date'].value_counts())
print(df['Months'].value_counts().keys().to_list())
# print(df['Year'].value_counts())


axes, fig = plt.subplots(4,3, figsize=(12,10))

for i in df['Months'].value_counts().keys().to_list():
    Jan = df[df['Months']==i]
    Date = Jan['Date']
    plt.title(label=f'{i} month analysis')
    sns.scatterplot(data=Jan,x='Date',
            y='Temp_C',hue='Temp_C')
    plt.xticks(rotation=45, ha='left') 
    plt.tight_layout(pad=2.0)
    plt.show()











