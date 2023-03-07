import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# start = datetime(2023, 2, 7, 7)
# end = datetime(2023, 2, 7, 8)
# unit = 26256679

def sensorTracing(unit, start, end):
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 5,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'reportObjectIdList': 0,
        'interval': {
            'from': int(start),
            'to': int(end),
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
    df.rename(columns={0: 'speed', 1: 'coordinates', 2: 'time', 3: 'volTotalIngreso', 4: 'volTotalRetorno', 5: 'volDifTotalAbsolute', 6: 'volDifTotalCus', 7: 'caudalIngreso', 8: 'caudalRetorno', 9: 'consumoCaudal', 10: 'horasIngresoAbsolute', 11: 'horasIngresoCus', 12: 'voltaje', 13: 'err', 14: 'info', 15: 'pitchAngle', 16: 'rollAngle', 17: 'volFuelRalenti', 18: 'volFuelOptimo', 19: 'volFuelSobrecarga', 20: 'horasRalenti', 21: 'horasOptimo'}, inplace=True)
    df['speed'] = df['speed'].apply(lambda x: 0 if x == "------" else x.split(' ')[0]).astype(float)
    df['volTotalIngreso'] = df['volTotalIngreso'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volTotalRetorno'] = df['volTotalRetorno'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volDifTotalAbsolute'] = df['volDifTotalAbsolute'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volDifTotalCus'] = df['volDifTotalCus'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['caudalIngreso'] = df['caudalIngreso'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['caudalRetorno'] = df['caudalRetorno'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['consumoCaudal'] = df['consumoCaudal'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['horasIngresoAbsolute'] = df['horasIngresoAbsolute'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['horasIngresoCus'] = df['horasIngresoCus'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['voltaje'] = df['voltaje'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['err'] = df['err'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['info'] = df['info'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['pitchAngle'] = df['pitchAngle'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['rollAngle'] = df['rollAngle'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volFuelRalenti'] = df['volFuelRalenti'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volFuelOptimo'] = df['volFuelOptimo'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['volFuelSobrecarga'] = df['volFuelSobrecarga'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['horasRalenti'] = df['horasRalenti'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    df['horasOptimo'] = df['horasOptimo'].apply(lambda x: 0 if x == "-----" else x).astype(float)
    return df
# sdk.logout()
