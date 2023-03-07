from calendar import month
import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta

resources = getResources()

start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end = datetime.now()
unit = 26256679


def reportGeofence(unit, start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 3,
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
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }

    rowsRutaPCh = sdk.report_get_result_rows(paramsRutaPCh)
    dataRutaPCh = [r['c'] for r in rowsRutaPCh]
    df = pd.DataFrame(dataRutaPCh)

    df.rename(columns={0: 'tripFrom', 1: 'tripTo', 2: 'begin', 3: 'end', 4: 'mileage', 5: 'duration', 6: 'avgSpeed', 7: 'maxSpeed',
                                8: 'consumed', 9: 'avgConsumed'}, inplace=True)
    df['trip'] = df['tripFrom'] + ' - ' + df['tripTo']
    df['dateBegin'] = pd.to_datetime(df['begin'].apply(lambda x: x['t']))
    df['mBegin'] = df['begin'].apply(lambda x: x['v'])
    df['xBegin'] = df['begin'].apply(lambda x: x['x'])
    df['yBegin'] = df['begin'].apply(lambda x: x['y'])
    df['dateEnd'] = pd.to_datetime(df['end'].apply(lambda x: x['t']))
    df['mEnd'] = df['end'].apply(lambda x: x['v'])
    df['xEnd'] = df['end'].apply(lambda x: x['x'])
    df['yEnd'] = df['end'].apply(lambda x: x['y'])
    df['mileage'] = df['mileage'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['duration'] = df['duration'].astype(float)
    df['avgSpeed'] = df['avgSpeed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['maxSpeed'] = df['maxSpeed'].apply(lambda x: x['t'].split(' ')[0]).astype(float)
    df['consumed'] = df['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgConsumed'] = df['avgConsumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    return df

# pd.set_option('display.max_rows', None)
