import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# start = datetime(2022, 7, 1, 7, 30, 00)
# end = datetime(2022, 7, 1, 8, 10, 49)
# unit = 25642783

def getSummary(unit, start, end):

    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 6,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'reportObjectIdList': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    paramsSummary = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    rows = sdk.report_get_result_rows(paramsSummary)
    dataSummary = [r['c'] for r in rows]
    df = pd.DataFrame(dataSummary)

    df.rename(columns={0: 'mileage', 1: 'avgSpeed', 2: 'maxSpeed', 3: 'moveTime', 4: 'engineTime', 5: 'parking', 6: 'consumed', 7: 'avgConsumed'}, inplace=True)
    df['mileage'] = df['mileage'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgSpeed'] = df['avgSpeed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['maxSpeed'] = df['maxSpeed'].apply(lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(float)
    df['moveTime'] = df['moveTime'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['engineTime'] = df['engineTime'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['parking'] = df['parking'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['consumed'] = df['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgConsumed'] = df['avgConsumed'].apply(lambda x: x.split(' ')[0]).astype(float)

    return df
# sdk.logout()
