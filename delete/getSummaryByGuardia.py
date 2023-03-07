# MODELO QUE ARREGLA EL DE WIALON YA QUE ESTA ROTO

import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# start = datetime(2022, 7, 1)
# end = datetime.now()


def getSummaryByGuardia(unit, start, end):

    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    df = pd.DataFrame()
    arr = []
    days = end - start
    n = days.total_seconds()/(24*3600)
    for i in range(((int(n) + 1) * 2)-1):
        paramsExecReport = {
            'reportResourceId': resources['items'][0]['id'],
            'reportTemplateId': 3,
            'reportObjectId': unit,
            'reportObjectSecId': 0,
            'reportObjectIdList': 0,
            'interval': {
                'from': int((start + timedelta(hours=(7 + (i*12)), minutes=30)).timestamp()),
                'to': int((start + timedelta(hours=(7 + ((i+1)*12)), minutes=30)).timestamp()),
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
        arr.extend(dataSummary)
    df = pd.DataFrame(arr)

    # df.rename(columns={0: 'group', 1: 'ratio', 2: 'parkingHours', 3: 'engineHours',
    #                           4: 'utilizado', 5: 'mileage', 6: 'avgSpeed', 7: 'maxSpeed', 8: 'moveTime', 9: 'engineTime', 10: 'parking', 11: 'consumed', 12: 'avgConsumed'}, inplace=True)
    # df['datetime'] = pd.to_datetime(df['group'])
    # df['ratio'] = df['ratio'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['parkingHours'] = df['parkingHours'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['engineHours'] = df['engineHours'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['utilizado'] = df['utilizado'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['mileage'] = df['mileage'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['avgSpeed'] = df['avgSpeed'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['maxSpeed'] = df['maxSpeed'].apply(
    #     lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(float)
    # df['consumed'] = df['consumed'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)
    # df['avgConsumed'] = df['avgConsumed'].apply(
    #     lambda x: x.split(' ')[0]).astype(float)

    return df
# sdk.logout()
