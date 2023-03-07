from main import login
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta, timezone
import time

from getSummary import getSummary
from getUnit import getUnits

df = pd.read_csv('data2/ciclo2.csv')
df['Starttime'] = pd.to_datetime(df['Starttime'])
df['Endtime'] = pd.to_datetime(df['Endtime'])
df = df.sort_values(by="Starttime")
# # FORMATO FECHA PYTHON MES/DIA/ANO para QUERY

units = getUnits()
# df = df.query('Starttime > "08/02/2022 13:57:26"')


arr = []
err = []
count = 0
for i, r in df.iterrows():
    start = r['Starttime'].tz_localize(tz='America/Lima')
    end = r['Endtime'].tz_localize(tz='America/Lima')
    truck = r['Eqm']
    # print(i)
    unit = [u['id'] for u in units['items'] if u['nm'] == truck]
    data = getSummary(unit[0], start, end)
    arr.extend(data.to_dict(orient='records'))
    # try:
    # except:
    #     print('Error: ', truck, start, end)
    #     arr.extend([{'mileage': 0, 'avgSpeed': 0, 'maxSpeed': 0, 'moveTime': 0, 'engineTime': 0, 'parking': 0, 'consumed': 0, 'avgConsumed': 0}])
    #     err.extend([{'truck': truck, 'start': start, 'end': end}])
    #     continue
    count += 1
    if(count == 40):
        time.sleep(40)
        count = 0
df2 = pd.DataFrame(arr)
df.reset_index(inplace=True)

_df = pd.concat([df, df2], axis=1)
_df.dropna(inplace=True)

# ADD RELATIONALS

# _df.query('Starttime < "07/05/2022"', inplace=True)


# unit = 25642783
# start = datetime(2022, 6, 20, 10, 3)
# end = datetime(2022, 6, 20, 10, 12) + timedelta(minutes=1)
# a = getSummary(unit, start, end)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# [{'nm': 'CM101', 'cls': 2, 'id': 25642783, 'mu': 0, 'uacl': 19327369763},
#  {'nm': 'CM121', 'cls': 2, 'id': 25642778, 'mu': 0, 'uacl': 19327369763}]
