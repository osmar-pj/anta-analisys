import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from getUnit import getUnits
from getTripsTest import getTripsTest
from getResumenByDia import getResumenByDia

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
model = Lasso()

start = datetime(2022, 4, 1)
end = datetime.now()

units = getUnits()

# GEOFENCES RUTA COMBUSTIBLE PARA HIDROGEN
arrRutaPCh = []
for u in units['items']:
    unit = u['id']
    dfRutaPCh, dfRutaPoints = getTripsTest(unit)
    dfRutaPCh['nm'] = u['nm']
    arrRutaPCh.extend(dfRutaPCh.to_dict(orient='records'))
df = pd.DataFrame(arrRutaPCh)

df = pd.read_csv('totalData.csv')

df1 = df.query('trip == "REFERENCE_PALA - STK2"').query('consumed < 60').query('ratio > 100')
df2 = df.query('trip == "REFERENCE_PALA - CHANCADO I"').query('consumed < 55').query('ratio > 100')
df3 = df.query('trip == "REFERENCE_PALA - STK7"').query('consumed < 100').query('ratio > 100')
df4 = df.query('trip == "992 - WASTE1"').query('consumed > 24').query('ratio > 100')

df_muestra = pd.concat([df1, df2, df3, df4])
_df = df[['parkingDuration', 'tripDuration', 'ratio', 'mileage', 'avgSpeed', 'maxSpeed', 'avgConsumed', 'consumed', 'nm']]

# PARA ENTRENAMIENTO DE MACHINE LEARNING
df_ml = df_muestra[['parkingDuration', 'tripDuration', 'ratio', 'mileage', 'avgSpeed', 'maxSpeed', 'avgConsumed', 'consumed', 'nm']]
df1_ml = df_ml.query('nm == "CAM-101"')
df2_ml = df_ml.query('nm == "CAM-121"')


X = _df
y = X['consumed']
x = X.drop(['consumed', 'nm'], axis=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
model.fit(x_train, y_train)
predicted = model.predict(x_test)
plt.hist([predicted, y_test])
model.score(x_test, y_test)

residuals = y_test - predicted
plt.scatter(y_test, residuals)

ap_residuals = np.abs(residuals) / y_test
plt.scatter(y_test, ap_residuals)

lap_residuals = np.log(ap_residuals)
plt.scatter(y_test, lap_residuals)

plt.hist(lap_residuals, bins=100, histtype='step', cumulative=True)
# df.to_csv('totalData.csv', index=False)

# df1 RUTA REFERENCE_PALA - STK2
# df1 = df.query('trip == "REFERENCE_PALA - STK2"').query('consumed < 60').query('ratio > 100')
# df2 = df.query('trip == "REFERENCE_PALA - CHANCADO I"').query('consumed < 55').query('ratio > 100')
# df3 = df.query('trip == "REFERENCE_PALA - STK7"').query('consumed < 100').query('ratio > 100')
# df4 = df.query('trip == "992 - WASTE1"').query('consumed > 24').query('ratio > 100')

# sns.scatterplot(data=df1, x='datetimeEnd', y='consumed', hue='nm')
# sns.scatterplot(data=df2, x='datetimeEnd', y='consumed', hue='nm')
# sns.scatterplot(data=df3, x='datetimeEnd', y='consumed', hue='nm')
# sns.scatterplot(data=df4, x='datetimeEnd', y='consumed', hue='nm')

# sns.scatterplot(data=df1, x='ratio', y='avgSpeed', hue='nm')
# sns.scatterplot(data=df2, x='ratio', y='avgSpeed', hue='nm')
# sns.scatterplot(data=df3, x='ratio', y='avgSpeed', hue='nm')
# sns.scatterplot(data=df4, x='ratio', y='avgSpeed', hue='nm')

# df1.to_csv('df1.csv', index=False)
# df2.to_csv('df2.csv', index=False)
# df3.to_csv('df3.csv', index=False)
# df4.to_csv('df4.csv', index=False)

# pd.set_option('display.max_rows', None)

# RESUMEN
# class places():
#     def __init__(self, id, nm):
#         self.id = id
#         self.nm = nm

# # to calculate every day
# arrDay = []
# for u in units['items']:
#     unit = u['id']
#     df = getResumenByDia(unit, start, end)
#     df['nm'] = u['nm']
#     arrDay.extend(df.to_dict(orient='records'))

# to calculate disponibildad
# arrDisp = []
# for p in places: