from main import login
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta, timezone

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
model = LinearRegression()

df = pd.read_csv('dft.csv')
df['Starttime'] = pd.to_datetime(df['Starttime'], dayfirst=True)
df['Endtime'] = pd.to_datetime(df['Endtime'], dayfirst=True)
df.query('Starttime < "07-01-2022"', inplace=True)

df['weekStart'] = df['Starttime'].apply(lambda x: x.isocalendar()[1])
df['monthStart'] = df['Starttime'].apply(lambda x: x.month)
df['dayStart'] = df['Starttime'].apply(lambda x: x.day)
df['hourStart'] = df['Starttime'].apply(lambda x: x.hour)
# df['minuteStart'] = df['Starttime'].apply(lambda x: x.minute)
# df['secondStart'] = df['Starttime'].apply(lambda x: x.second)

df['weekEnd'] = df['Endtime'].apply(lambda x: x.isocalendar()[1])
df['monthEnd'] = df['Endtime'].apply(lambda x: x.month)
df['dayEnd'] = df['Endtime'].apply(lambda x: x.day)
df['hourEnd'] = df['Endtime'].apply(lambda x: x.hour)
# df['minuteEnd'] = df['Endtime'].apply(lambda x: x.minute)
# df['secondEnd'] = df['Endtime'].apply(lambda x: x.second)

# get day monday or friday
df['day'] = df['Starttime'].apply(lambda x: x.strftime('%A'))
df['month'] = df['Starttime'].apply(lambda x: x.strftime('%B'))

df['moveTime'] = df['moveTime'] * 60
df['parking'] = df['parking'] * 60
df['engineTime'] = df['engineTime'] * 60
#	Travelling Empty (min) Queuing at Source (min)	Spotting at Source (min)	Waiting for Load (min)	Loading (min)	Travelling Full (min)	Queueing at Sink (min)	Spotting at Sink (min)	Dumping (min)
df['tripTime'] = (df['Travelling Empty (min)'] + df['Queuing at Source (min)'] + df['Spotting at Source (min)'] + df['Waiting for Load (min)'] + df['Loading (min)'] + df['Travelling Full (min)'] + df['Queueing at Sink (min)'] + df['Spotting at Sink (min)'] + df['Dumping (min)'])
df.rename(columns={'Distance Average (km)': 'avgMileage', 'Travelling Empty (min)': 'travelingEmpty','Queuing at Source (min)': 'queuingSource', 'Spotting at Source (min)': 'spottingSource', 'Waiting for Load (min)': 'waitingLoad', 'Loading (min)': 'loading','Travelling Full (min)': 'travelingFull', 'Queueing at Sink (min)': 'queuingSink', 'Spotting at Sink (min)': 'spottingSink', 'Dumping (min)': 'dumping'}, inplace=True)

# df['delta_time'] = df['moveTime'] - df['tripTime']
# df['delta_distance'] = df['mileage'] - (df['avgMileage'] * 2)

df['gal_ktonkm'] = df['consumed']*10000/(df['Tons']*df['mileage'])
# df['gal_km'] = df['consumed']/(df['mileage'])
# df['gal_ton'] = df['consumed']/(df['Tons'])
# df['ton_km_gal'] = df['Tons']/df['mileage']/df['consumed']
# df['ton_gal_km'] = df['Tons']/df['consumed']/df['mileage']
df['trip'] = df['Source'] + ' - ' + df['Destination']
df['trip_truck'] = df['Shovel/Loader'] + ' - ' + df['Destination']
# drop column
# df['deltaTime'] = (df['Endtime'] - df['Starttime']).apply(lambda x: x.value*60/3600000000000)
# df['ratio'] = df['consumed'] / df['tripTime']
# Queuing at Source (min)	Spotting at Source (min)	Waiting for Load (min)	Loading (min)	Travelling Full (min)	Queueing at Sink (min)	Spotting at Sink (min)	Dumping (min)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# [{'nm': 'CM101', 'cls': 2, 'id': 25642783, 'mu': 0, 'uacl': 19327369763},
#  {'nm': 'CM121', 'cls': 2, 'id': 25642778, 'mu': 0, 'uacl': 19327369763}]

# VIAJES CARGADOS APARENTEMENTE 0
df1 = df.query('travelingFull == 0')
df.query('travelingFull != 0', inplace=True)
# MUY BAJO TONELAJE MENORES DE 100
df2 = df.query('Tons < 100')
df.query('Tons > 100', inplace=True)
# VIAJES MUY CORTOS < 50m
df3 = df.query('avgMileage < 0.05')
df.query('avgMileage > 0.05', inplace=True)
# GAL/KTON KM MUY BAJO Y MUY ALTO
df4 = df.query('gal_ktonkm > 50')
df5 = df.query('gal_ktonkm < 0.1')
df.query('gal_ktonkm < 50 or gal_ktonkm > 0.1', inplace=True)
# df.query('avgConsumed < 1.5', inplace=True)
# df.query('tripTime > 6', inplace=True)

# ANALISIS
df.groupby(['Truck', 'month'])['gal_ktonkm'].mean()
df.groupby(['Truck', 'day'])['gal_ktonkm'].mean()
df.groupby(['Truck', 'Guardia'])['gal_ktonkm'].mean()
df.groupby(['Truck', 'Operator']).mean()

# _df.sort_values(by=['Truck', 'gal_ktonkm'])
df.query('Operator == "Apolinario Caushi, Ever Jonatan"')

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


# NAALISIS ANDRE
df.query('trip_truck == "PL003 - Chancadora Primaria"').groupby(['Guardia', 'Operator', 'Truck']).count().sort_values(by=['gal_ktonkm'], ascending=False)
df1 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Orccoapaza Quispe, Adrian" and Truck == "CM101"')
df2 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Machacuay Tinoco, Rufilio Julio" and Truck == "CM101"')
df3 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Vasquez Briceno, Neylser Alexander" and Truck == "CM101"')
df4 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Condori Nina, Ricardo Moises" and Truck == "CM121"')
df5 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Lucas Cabello, Wilmer Joel" and Truck == "CM121"')
df6 = df.query('trip_truck == "PL003 - Chancadora Primaria"').query('Operator == "Gutierrez Cisneros, Richar Efrain" and Truck == "CM121"')
# Join df1 al df6
df7 = pd.concat([df1, df2, df3, df4, df5, df6])
df7.groupby(['Operator', 'Truck']).mean()