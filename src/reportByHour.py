import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# start = datetime(2022, 12, 15)
# end = datetime(2022, 12, 16, 23, 59, 59)
# unit = 26256679

def reportByHour(unit, start, end):
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 1,
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
    dfSummary.rename(columns={0: 'datetime', 1: 'mileage', 2: 'avgSpeed', 3: 'maxSpeed', 4: 'moveTime', 5: 'engineTime', 6: 'parking', 7: 'consumed', 8: 'avgConsumed'}, inplace=True)
    dfSummary['parking'] = dfSummary['parking'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['engineTime'] = dfSummary['engineTime'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfSummary['moveTime'] = dfSummary['moveTime'].apply(
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

    paramSensor = {
        'tableIndex': 1,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][1]['rows']
    }
    rows = sdk.report_get_result_rows(paramSensor)
    dataSensor = [r['c'] for r in rows]
    dfSensor = pd.DataFrame(dataSensor)
    dfSensor.rename(columns={0: 'datetime', 1: 'initialPitchAngle', 2: 'initialRollAngle', 3: 'initialVolFuelRalenti', 4: 'initialVolFuelOptimo', 5: 'initialVolSobrecarga', 6: 'initialHorasRalenti', 7: 'initialHorasOptimo', 8: 'finalPitchAngle', 9: 'finalRollAngle', 10: 'finalVolFuelRalenti', 11: 'finalVolFuelOptimo', 12: 'finalVolFuelSobrecarga', 13: 'finalHorasRalenti', 14: 'finalHorasOptimo'}, inplace=True)
    dfSensor['initialPitchAngle'] = dfSensor['initialPitchAngle'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialRollAngle'] = dfSensor['initialRollAngle'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialVolFuelRalenti'] = dfSensor['initialVolFuelRalenti'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialVolFuelOptimo'] = dfSensor['initialVolFuelOptimo'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialVolSobrecarga'] = dfSensor['initialVolSobrecarga'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialHorasRalenti'] = dfSensor['initialHorasRalenti'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['initialHorasOptimo'] = dfSensor['initialHorasOptimo'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalPitchAngle'] = dfSensor['finalPitchAngle'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalRollAngle'] = dfSensor['finalRollAngle'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalVolFuelRalenti'] = dfSensor['finalVolFuelRalenti'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalVolFuelOptimo'] = dfSensor['finalVolFuelOptimo'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalVolFuelSobrecarga'] = dfSensor['finalVolFuelSobrecarga'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalHorasRalenti'] = dfSensor['finalHorasRalenti'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['finalHorasOptimo'] = dfSensor['finalHorasOptimo'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfSensor['fuelRalenti'] = dfSensor['finalVolFuelRalenti'] - dfSensor['initialVolFuelRalenti']
    dfSensor['fuelOptimo'] = dfSensor['finalVolFuelOptimo'] - dfSensor['initialVolFuelOptimo']
    dfSensor['fuelTotal'] = dfSensor['fuelRalenti'] + dfSensor['fuelOptimo']
    dfSensor['horasRalenti'] = dfSensor['finalHorasRalenti'] - dfSensor['initialHorasRalenti']
    dfSensor['horasOptimo'] = dfSensor['finalHorasOptimo'] - dfSensor['initialHorasOptimo']
    dfSensor['horasTotal'] = dfSensor['horasRalenti'] + dfSensor['horasOptimo']

    # merge horizontal dfSummary and sfSensor by datetime
    df = pd.merge(dfSummary, dfSensor, on=['datetime'], how='outer')
    # remove () of datetime and convert to date and time
    return df
# sdk.logout()

# df = reportByHour(unit, start, end)