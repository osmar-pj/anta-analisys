# Corresponde a los datos de "Messages" del ORF con la opcion "Row Data" de "Show parameters as:"
# los datos de guardan en reports y se crea un DF para mejor visualizacion y procesamiento
# Funciona para unidad "unit"

import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources
from getUnit import getUnits

start = datetime(2022, 12, 7)
end = datetime.now()
unit = 26256679

resources = getResources()
# units = getUnits()

# def getSummaryByDay(unit, start, end):

sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

params = {
    'itemId': unit,
    'lastTime': 0,
    'lastCount': 10,
    'flags': 0,
    'flagsMask': 0,
    'loadCount': 10,
}
reports = sdk.messages_load_last(params)
df = pd.DataFrame(reports['messages'])

# return reports
# sdk.logout()
