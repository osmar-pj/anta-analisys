import pandas as pd

from disponibilidad import disponibilidad
from getResumenByDia import getResumenByDia
from getUnit import getUnits

# start = datetime(2022, 6, 1)
# end = datetime.now()

def operaciones(start, end):
    disp = disponibilidad(start, end)
    # disp = pd.read_csv('disp.csv')
    disp['delta'] = disp['datetimeOut'].apply(lambda x: x.strftime('%d')).astype(int) - disp['datetimeIn'].apply(lambda x: x.strftime('%d')).astype(int)
    idx = disp.delta > 0
    filtered = disp[idx]

    d1 = disp.copy()
    df1 = pd.DataFrame().reindex_like(d1).dropna(inplace=False)
    count = 0
    for i,f in enumerate(filtered.T):
        delta = filtered['delta'][f]
        midnight = [filtered['datetimeOut'][f].replace(hour=0, minute=0, second=0) for j in range(delta)]
        dates = [filtered['datetimeIn'][f], midnight[0], filtered['datetimeOut'][f]]
        for d in range(len(dates) - 1):
            duration = (dates[d + 1] - dates[d]).total_seconds() / 3600
            unit = filtered['unit'][f]
            timeIn = filtered['timeIn'][f]
            timeOut = filtered['timeOut'][f]
            durationIn = filtered['durationIn'][f]
            parkingDuration = filtered['parkingDuration'][f]
            offTime = filtered['offTime'][f]
            mileage = filtered['mileage'][f]
            consumed = filtered['consumed'][f]
            avgConsumed = filtered['avgConsumed'][f]
            zone = filtered['zone'][f]
            datetimeIn = dates[0 + d]
            datetimeOut = dates[1 + d]
            delta = filtered['delta'][f]
            df1.loc[count] = [duration, unit, timeIn, timeOut, durationIn, parkingDuration, offTime, mileage, consumed, avgConsumed, zone, datetimeIn, datetimeOut, delta]
            count+=1


    idx1 = disp.delta < 1
    disp = disp[idx1]
    disp = disp.append(df1).reset_index()
    disp['date'] = pd.to_datetime(disp['datetimeIn'].apply(lambda x: x.date()))
    disp['week'] = disp['datetimeIn'].apply(lambda x: x.week)
    disp['month'] = disp['datetimeIn'].apply(lambda x: x.month)


    units = getUnits()
    arrDate = []
    for unit in units['items']:
        unitId = unit['id']
        df = getResumenByDia(unitId, start, end)
        df['unit'] = unit['nm']
        arrDate.extend(df.to_dict(orient='records'))
    dfSum = pd.DataFrame(arrDate)
    dfSum['week'] = dfSum['datetime'].apply(lambda x: x.week)
    dfSum['month'] = dfSum['datetime'].apply(lambda x: x.month)

    d_date = (disp.query('indisponible > 0.02').groupby(['date', 'unit']).sum()).reset_index()
    d_date.drop(['mileage', 'consumed', 'avgConsumed', 'delta', 'week', 'month', 'index'], axis=1, inplace=True)
    d_date.rename(columns={'date': 'datetime'}, inplace=True)

    df = pd.merge(d_date, dfSum, on=['datetime', 'unit'], how='outer')
    df.fillna(0, inplace=True)

    df['disponibilidad'] = (24 - df['indisponible']) / 24
    df['uso disponibilidad'] = df['utilizado'] / (24 - df['indisponible'])
    df['utilizacion'] = df['utilizado'] / 24
    df.query('engineHours < 24', inplace=True)
    df.sort_values(by=['datetime'], inplace=True)
    return df
    