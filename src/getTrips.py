import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources
from getUnit import getUnits

start = datetime(2022, 12, 7)
end = datetime.now()
unit = 26256679
resources = getResources()
units = getUnits()

# def getSummaryByDay(unit, start, end):

sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

params = {
    'itemId': unit,
    'msgsSource': 0,
    'timeFrom': int(start.timestamp()),
    'timeTo': int(end.timestamp())
}
reports = sdk.unit_get_trips(params)

# return reports
# sdk.logout()
