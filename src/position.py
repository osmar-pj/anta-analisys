import pandas as pd
from main import login
from getUnit import getUnits
from datetime import datetime, timedelta
from getResource import getResources

units = getUnits()
resources = getResources()

def position():
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }

    sdk.render_set_locale(parameterSetLocale)

    unit = [u['id'] for u in units['items']]

    paramUbication = {
        'spec': [{'type': 'col', 'data': unit, 'flags': 4194304, 'mode': 0}]
    }
        
    resUbication = sdk.core_update_data_flags(paramUbication)

    a = pd.DataFrame(units['items'])
    b = pd.DataFrame(resUbication)
    b.rename(columns={'i': 'id'}, inplace=True)
    df = a.merge(b, on='id', how='left')
    # convert to dict
    # data = df.to_dict('records')
    return df

# end = datetime.now()
# start = end - timedelta(minutes=180)
# unit = 26256679

def realtime(unit, start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }

    sdk.render_set_locale(parameterSetLocale)
    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 2,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'reportObjectIdList': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 117440512
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    paramsSummary = {
        'tableIndex': 2,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][2]['rows']
    }
    rows = sdk.report_get_result_rows(paramsSummary)
    dataSummary = [r['c'] for r in rows]
    df = pd.DataFrame(dataSummary)
    return df
