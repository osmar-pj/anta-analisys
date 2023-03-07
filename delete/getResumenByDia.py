import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# start = datetime(2022, 7, 1)
# end = datetime.now()


def getResumenByDia(unit, start, end):

    sdk = login()
    resources = getResources()
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
    dfSummary = pd.DataFrame(dataSummary)

    dfSummary.rename(columns={0: 'group', 1: 'parkingHours', 2: 'engineHours',
                              3: 'utilizado', 4: 'mileage', 5: 'avgSpeed', 6: 'maxSpeed', 7: 'moveTime', 8: 'engineTime', 9: 'parking', 10: 'consumed', 11: 'avgConsumed'}, inplace=True)
    dfSummary['datetime'] = pd.to_datetime(dfSummary['group'])
    dfSummary['parkingHours'] = dfSummary['parkingHours'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['engineHours'] = dfSummary['engineHours'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['utilizado'] = dfSummary['utilizado'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['mileage'] = dfSummary['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['avgSpeed'] = dfSummary['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['maxSpeed'] = dfSummary['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(float)
    dfSummary['consumed'] = dfSummary['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['avgConsumed'] = dfSummary['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)

    return dfSummary
# sdk.logout()
