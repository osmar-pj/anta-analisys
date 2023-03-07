import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from getUnit import getUnits
from getAllTrips import getAllTrips

start = datetime(2022, 6, 10)
end = datetime(2022, 9, 9)
# end = datetime.now()
units = getUnits()
arr = []
for unit in units['items']:
    df = getAllTrips(unit['id'], start, end)
    df['nm'] = unit['nm']
    arr.extend(df.to_dict('records'))
df = pd.DataFrame(arr)
df['ratio'] = df['consumed'] / df['tripDuration']
df['eq'] = 'sin hidragen'
idx1 = df['datetimeBegin'].between(datetime(2022, 7, 1), datetime(2022, 8, 8))
df.loc[(idx1), 'eq'] = 'adaptacion'
idx2 = df['datetimeBegin'].between(datetime(2022, 8, 1), datetime(2022, 9, 5))
df.loc[(idx2), 'eq'] = 'con hidragen'

df = df.query('consumed < 250').query('consumed != 0')
df['rendimiento'] = df['mileage']/df['consumed']

# df1 = df.query('tripFrom == "REFERENCE_PALA"')
df1 = df.query('trip == "REFERENCE_PALA - CHANCADO I"')
df1 = df1.query('mileage < 4')
df1 = df1.query('consumed < 50')
df1 = df1.query('consumed > 40')
# df2 = df.query('trip == "REFERENCE_PALA - STK1"')
# df3 = df.query('trip == "REFERENCE_PALA - STK3"')
# df4 = df.query('trip == "REFERENCE_PALA - STK7"')
# df5 = df.query('trip == "REFERENCE_PALA - S3"')
# df6 = df.query('trip == "REFERENCE_PALA - EAST_DUMP"')
# df7 = df.query('trip == "REFERENCE_PALA - STK5"')
df8 = df.query('trip == "REFERENCE_PALA - STK2"')
# df9 = df.query('trip == "REFERENCE_PALA - S2"')
# df10 = df.query('trip == "REFERENCE_PALA - LT03"')
# df11 = df.query('trip == "REFERENCE_PALA - BUENAVENTURA"')
# df12 = df.query('trip == "REFERENCE_PALA - LODOS"')


# df.drop_duplicates(subset=['trip']).query('tripFrom == "REFERENCE_PALA"')

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)