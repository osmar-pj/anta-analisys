import pandas as pd
from datetime import datetime, timedelta

from getUnit import getUnits
from getGeofence import getGeofences
from getZones import getZones

# start = datetime(2022, 7, 1)
# end = datetime.now()

units = getUnits()
zones = getZones()

manttoZones = ['AK15', 'BUENAVENTURA', 'PARQUEO01', 'TRUCKSHOP']
# filter manttoZones values from zones
zonesFiltered = [zone for zone in zones if zone['n'] in manttoZones]

# to calculate every day
def disponibilidad(start, end):
    arrZones = []
    for z in zonesFiltered:
        zoneId = z['id']
        dfZones = getGeofences(zoneId, start, end)
        dfZones['zone'] = z['n']
        arrZones.extend(dfZones.to_dict(orient='records'))
    df = pd.DataFrame(arrZones)
    df.rename(columns={0: 'indisponible', 1: 'unit', 2: 'timeIn', 3: 'timeOut', 4: 'durationIn', 5: 'parkingDuration', 6: 'offTime', 7: 'mileage', 8: 'consumed', 9: 'avgConsumed'}, inplace=True)
    df['indisponible'] = df['indisponible'].astype(float)
    df['datetimeIn'] = pd.to_datetime(df['timeIn'].apply(lambda x: x['t']))
    df['datetimeOut'] = pd.to_datetime(df['timeOut'].apply(lambda x: x['t']))
    df['mileage'] = df['mileage'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['consumed'] = df['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgConsumed'] = df['avgConsumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    return df