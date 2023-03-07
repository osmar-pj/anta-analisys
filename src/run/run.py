import schedule
import time
import pandas as pd
from datetime import datetime, timedelta
from getUnit import getUnits
from reportByDay import reportByDay
from reportByHour import reportByHour

def updateData():
    print('starting...')
    start = datetime.now() - timedelta(weeks=10)
    end = datetime.now()
    # unit = 10265

    units = getUnits()
    arr = []

    for unit in units['items']:
        try:
            _df = reportByDay(unit['id'], start, end)
            _df['nm'] = unit['nm']
            arr.extend(_df.to_dict('records'))
        except:
            print('error')
    df = pd.DataFrame(arr)
    df.to_csv('../day.csv', index=False)
    return

# updateData()
# schedule.every().saturday.at("00:01").do(updateData)
schedule.every().day.at("11:52").do(updateData)

while True:
    schedule.run_pending()
    time.sleep(1)
