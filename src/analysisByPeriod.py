import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from reportByDay import reportByDay
from reportByHour import reportByHour
from reportGeofence import reportGeofence
from sensorTracing import sensorTracing
from getUnit import getUnits
from position import position
from hourData import getHourData

import time

# 'items': [  {'nm': 'HT57', 'cls': 2, 'id': 26243338, 'mu': 3, 'uacl': 19327369763},
#             {'nm': 'HT61', 'cls': 2, 'id': 26256679, 'mu': 3, 'uacl': 19327369763},
#             {'nm': 'HT62', 'cls': 2, 'id': 26258342, 'mu': 3, 'uacl': 19327369763}]}

# HT57 period -> 07-12-2022
# HT61 period -> 07-12-2022
# HT62 period -> 07-12-2022

start = datetime(2022, 12, 7)
end = datetime.now().replace(minute=59, second=59, microsecond=9999) - timedelta(hours=1)
# unit = 26258342
# df = sensorTracing(unit, start, end)
# df = reportGeofence(unit, start, end)
units = getUnits()
# df = getHourData(start, end)
# df = pd.DataFrame()
# for unit in units['items']:
#     try:
#         df_geo = reportGeofence(unit['id'], start, end)
#         df_geo['nm'] = unit['nm']
#         df = df.append(df_geo, ignore_index=True)
#     except:
#         print('error')




# df.to_csv('./data/hour.csv', index=False)

# # df.query("`{0}` > 10".format(a))
        