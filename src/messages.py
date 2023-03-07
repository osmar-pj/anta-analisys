import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

start = datetime(2023, 2, 4)
end = datetime.now()
unit = 26256679

# 'items': [  {'nm': 'HT57', 'cls': 2, 'id': 26243338, 'mu': 3, 'uacl': 19327369763},
#             {'nm': 'HT61', 'cls': 2, 'id': 26256679, 'mu': 3, 'uacl': 19327369763},
#             {'nm': 'HT62', 'cls': 2, 'id': 26258342, 'mu': 3, 'uacl': 19327369763}]}

# def getSummaryByDay(unit, start, end):

sdk = login()
resources = getResources()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

params = {
    'layerName': 'messages',
    'itemId': 26256679,
    'timeFrom': int(start.timestamp()),
    'timeTo': int(end.timestamp()),
    'flags': 0,
    'tripDetector': 0,
    'trackWidth': 4,
    'trackColor': 'sensor',
    'annotations:' : 0,
    'points': 1,
    'pointColor': "cc0000ff",
    'arrows': 1
}

report = sdk.render_create_messages_layer(params)

# params = {
#     'layerName': 'messages',
#     'indexFrom': 0,
#     'indexTo': 1000,
#     'unitId': 26256679
#  }

# report = sdk.render_get_messages(params)

# paramsExecReport = {
#     'reportResourceId': resources['items'][0]['id'],
#     'reportTemplateId': 2,
#     'reportObjectId': unit,
#     'reportObjectSecId': 0,
#     'reportObjectIdList': 0,
#     'interval': {
#         'from': int(start.timestamp()),
#         'to': int(end.timestamp()),
#         'flags': 0
#     }
# }
# reports = sdk.report_exec_report(paramsExecReport)
# paramsSummary = {
#     'tableIndex': 0,
#     'indexFrom': 0,
#     'indexTo': reports['reportResult']['tables'][0]['rows']
# }
# rows = sdk.report_get_result_rows(paramsSummary)
# data = [r['c'] for r in rows]
# df = pd.DataFrame(data)

# df.rename(columns={0: 'group', 1: 'mileage', 2: 'avgSpeed', 3: 'maxSpeed', 4: 'moveTime', 5: 'engineTime', 6: 'parking', 7: 'consumed', 8: 'avgConsumed'}, inplace=True)
# df['date'] = df['group'].apply(lambda x: x.split(')')[0].split('(')[1])
# df['date'] = pd.to_datetime(df['date'])
# df['turn'] = df['group'].apply(lambda x: x.split(' ')[1])
# df['parking'] = df['parking'].apply(
#     lambda x: x.split(' ')[0]).astype(float)
# df['engineTime'] = df['engineTime'].apply(
#     lambda x: x.split(' ')[0]).astype(float)
# df['moveTime'] = df['moveTime'].apply(
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

    # return df
# sdk.logout()
