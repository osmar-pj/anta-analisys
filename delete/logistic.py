from main import login
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta, timezone

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
model = LinearRegression()

df = pd.read_csv('_dfv2.csv')
df['Starttime'] = pd.to_datetime(df['Starttime'], dayfirst=True)
df['Endtime'] = pd.to_datetime(df['Endtime'], dayfirst=True)

df['weekStart'] = df['Starttime'].apply(lambda x: x.isocalendar()[1])
df['monthStart'] = df['Starttime'].apply(lambda x: x.month)
df['dayStart'] = df['Starttime'].apply(lambda x: x.day)
df['hourStart'] = df['Starttime'].apply(lambda x: x.hour)
df['minuteStart'] = df['Starttime'].apply(lambda x: x.minute)
df['secondStart'] = df['Starttime'].apply(lambda x: x.second)

df['weekEnd'] = df['Endtime'].apply(lambda x: x.isocalendar()[1])
df['monthEnd'] = df['Endtime'].apply(lambda x: x.month)
df['dayEnd'] = df['Endtime'].apply(lambda x: x.day)
df['hourEnd'] = df['Endtime'].apply(lambda x: x.hour)
df['minuteEnd'] = df['Endtime'].apply(lambda x: x.minute)
df['secondEnd'] = df['Endtime'].apply(lambda x: x.second)

df['moveTime'] = df['moveTime'] * 60
df['parking'] = df['parking'] * 60
df['engineTime'] = df['engineTime'] * 60
#	Travelling Empty (min) Queuing at Source (min)	Spotting at Source (min)	Waiting for Load (min)	Loading (min)	Travelling Full (min)	Queueing at Sink (min)	Spotting at Sink (min)	Dumping (min)
df['tripTime'] = (df['Travelling Empty (min)'] + df['Queuing at Source (min)'] + df['Spotting at Source (min)'] + df['Waiting for Load (min)'] + df['Loading (min)'] + df['Travelling Full (min)'] + df['Queueing at Sink (min)'] + df['Spotting at Sink (min)'] + df['Dumping (min)'])
df.rename(columns={'Distance Average (km)': 'avgMileage', 'Travelling Empty (min)': 'travelingEmpty','Queuing at Source (min)': 'queuingSource', 'Spotting at Source (min)': 'spottingSource', 'Waiting for Load (min)': 'waitingLoad', 'Loading (min)': 'loading','Travelling Full (min)': 'travelingFull', 'Queueing at Sink (min)': 'queuingSink', 'Spotting at Sink (min)': 'spottingSink', 'Dumping (min)': 'dumping'}, inplace=True)
df['gal_tonkm'] = df['consumed']/(df['Tons']*df['mileage'])
df['gal_km'] = df['consumed']/(df['mileage'])
df['gal_ton'] = df['consumed']/(df['Tons'])
df['ton_km_gal'] = df['Tons']/df['mileage']/df['consumed']
df['ton_gal_km'] = df['Tons']/df['consumed']/df['mileage']
df['trip'] = df['Source'] + ' - ' + df['Destination']
# drop column
df['deltaTime'] = (df['Endtime'] - df['Starttime']).apply(lambda x: x.value*60/3600000000000)
df['ratio'] = df['consumed'] / df['tripTime']
# Queuing at Source (min)	Spotting at Source (min)	Waiting for Load (min)	Loading (min)	Travelling Full (min)	Queueing at Sink (min)	Spotting at Sink (min)	Dumping (min)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# [{'nm': 'CM101', 'cls': 2, 'id': 25642783, 'mu': 0, 'uacl': 19327369763},
#  {'nm': 'CM121', 'cls': 2, 'id': 25642778, 'mu': 0, 'uacl': 19327369763}]

# LIMPIEZA DE DATOS
df.query('travelingFull != 0', inplace=True)
df.query('tripTime > 6', inplace=True)


# DATOS CATEGORICOS
dummies = pd.get_dummies(df[['Operator', 'Source', 'Destination', 'Guardia', 'Shovel/Loader', 'Truck']])
_df = pd.concat([df, dummies], axis=1)

_df.drop(['Calendardate','Starttime', 'Endtime', 'Guardia', 'Source', 'Polygon', 'Destination', 'Shovel/Loader', 'Fleet', 'Truck', 'Operator', 'Cycles', 'trip'], axis=1, inplace=True)

# MODELAMIENTO LASSO
X = _df
y = X['consumed']
x = X.drop(['consumed'], axis=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
model.fit(x_train, y_train)

predicted = model.predict(x_test)
plt.hist([predicted, y_test])
model.score(x_test, y_test)

residuals = y_test - predicted
plt.scatter(y_test, residuals)


# sns.scatterplot(data=df1, x='mileage', y='consumed', hue='trip')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


ap_residuals = np.abs(residuals) / y_test
plt.scatter(y_test, ap_residuals)

lap_residuals = np.log(ap_residuals)
plt.scatter(y_test, lap_residuals)

plt.hist(lap_residuals, bins=100, histtype='step', cumulative=True)
