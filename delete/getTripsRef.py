import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta

resources = getResources()

# start = datetime(2022, 5, 22)
# end = datetime.now()
unit = 25642778


# def getTripsTest(unit):
end = datetime.now()
start = datetime(2022, 5, 1)
sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

paramsExecReport = {
    'reportResourceId': resources['items'][0]['id'],
    'reportTemplateId': 8,
    'reportObjectId': unit,
    'reportObjectSecId': 0,
    'interval': {
        'from': int(start.timestamp()),
        'to': int(end.timestamp()),
        'flags': 0
    }
}
reports = sdk.report_exec_report(paramsExecReport)

# TRIPS
# 6 TripsMine2Lima
paramsRutaPCh = {
    'tableIndex': 3,
    'indexFrom': 0,
    'indexTo': reports['reportResult']['tables'][3]['rows']
}

rowsRutaPCh = sdk.report_get_result_rows(paramsRutaPCh)
dataRutaPCh = [r['c'] for r in rowsRutaPCh]
df = pd.DataFrame(dataRutaPCh)

df.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                            8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
df['parkingDuration'] = pd.to_numeric(
    df['parkingDuration'], errors='coerce')
df['tripDuration'] = pd.to_numeric(
    df['tripDuration'], errors='coerce')
df['ratio'] = df['ratio'].apply(
    lambda x: x.split(' ')[0]).astype(float)
df['mileage'] = df['mileage'].apply(
    lambda x: x.split(' ')[0]).astype(float)
df['avgSpeed'] = df['avgSpeed'].apply(
    lambda x: x.split(' ')[0]).astype(float)
df['maxSpeed'] = df['maxSpeed'].apply(
    lambda x: x['t'].split(' ')[0]).astype(int)
df['consumed'] = df['consumed'].apply(
    lambda x: x.split(' ')[0]).astype(float)
df['avgConsumed'] = df['avgConsumed'].apply(
    lambda x: x.split(' ')[0]).astype(float)
df['timestampBegin'] = df['datetimeBegin'].apply(
    lambda x: x['v'])
df['datetimeBegin'] = pd.to_datetime(
    df['datetimeBegin'].apply(lambda x: x['t']))
df['timestampEnd'] = df['datetimeEnd'].apply(
    lambda x: x['v'])
df['datetimeEnd'] = pd.to_datetime(
    df['datetimeEnd'].apply(lambda x: x['t']))

    # return df

# # pd.set_option('display.max_rows', None)
# df1 = df.query('trip == "REF-PALA-Hidragen - CHANCADO I"').query('mileage < 4')
# df2 = df.query('trip == "REF-PALA-Hidragen - REF-STK7-Hidragen"').query('mileage < 7.5')
# df3 = df.query('trip == "992-Hidragen - WASTE-Hidragen"')