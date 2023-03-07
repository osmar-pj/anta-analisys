import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta

resources = getResources()

start = datetime(2023, 1, 26)
end = datetime.now()
unit = 26243338


# def getGeofences(zone, start, end):

sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

paramsExecReport = {
    'reportResourceId': resources['items'][0]['id'],
    'reportTemplateId': 3,
    'reportObjectId': resources['items'][0]['id'],
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
paramsDispo = {
    'tableIndex': 0,
    'indexFrom': 0,
    'indexTo': reports['reportResult']['tables'][0]['rows']
}

rowsDispo = sdk.report_get_result_rows(paramsDispo)
dataDispo = [r['c'] for r in rowsDispo]
dfDispo = pd.DataFrame(dataDispo)
    # return dfDispo

# pd.set_option('display.max_rows', None)
