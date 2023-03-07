import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta

resources = getResources()

# start = datetime(2022, 6, 1)
# end = datetime(2022, 8, 8)
# unit = 25642783


def getAllTrips(unit, start, end):
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
        'tableIndex': 1,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][1]['rows']
    }

    rowsRutaPCh = sdk.report_get_result_rows(paramsRutaPCh)
    dataRutaPCh = [r['c'] for r in rowsRutaPCh]
    df = pd.DataFrame(dataRutaPCh)

    df.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                                8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    df['parkingDuration'] = pd.to_numeric(df['parkingDuration'], errors='coerce')
    df['tripDuration'] = pd.to_numeric(df['tripDuration'], errors='coerce')
    df['ratio'] = df['ratio'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['mileage'] = df['mileage'].apply( lambda x: x.split(' ')[0]).astype(float)
    df['avgSpeed'] = df['avgSpeed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['maxSpeed'] = df['maxSpeed'].apply(lambda x: 0 if x == '0 km/h' else x['t'].split(' ')[0]).astype(float)
    df['consumed'] = df['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgConsumed'] = df['avgConsumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['timestampBegin'] = df['datetimeBegin'].apply(lambda x: x['v'])
    df['datetimeBegin'] = pd.to_datetime(df['datetimeBegin'].apply(lambda x: x['t']))
    df['timestampEnd'] = df['datetimeEnd'].apply(lambda x: x['v'])
    df['datetimeEnd'] = pd.to_datetime(df['datetimeEnd'].apply(lambda x: x['t']))


    return df

# pd.set_option('display.max_rows', None)
