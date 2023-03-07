import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

from getUnit import getUnits
from position import position
from reportByHour import reportByHour
from reportByDay import reportByDay
from reportGeofence import reportGeofence
from sensorTracing import sensorTracing
from getUnit import getUnits
from hourData import getHourData

app = Flask(__name__)
cors = CORS(app)

units = getUnits()
path = './run/data'

@app.route('/api/v1/dashboard', methods=['GET'])
def dashboard():
    # obtiene los valores de la unidad, parametro, periodo, patrones
    unit = request.args.get('unit')
    option = request.args.get('option')
    # parameter = request.args.get('parameter', default=None, type=int)
    period = request.args.get('period', default=None, type=int)
    pattern = request.args.get('pattern', default=None, type=int)
    print(unit, period, pattern)
    df = pd.read_csv('{}/hour.csv'.format(path))
    trip = pd.read_csv('{}/trip.csv'.format(path))
    df1 = df.copy()
    # convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if (option == 'period'):
        if period == 8:
            df = df.groupby(['year', 'month', 'nm', 'turn']).sum()
            df['ratio'] = df['consumed']/df['engineTime']
            df['avgConsumed'] = df['mileage']/df['consumed']
            df.reset_index(inplace=True)
        elif period == 7:
            df = df.groupby(['year_week', 'week', 'nm', 'turn']).sum()
            df['ratio'] = df['consumed']/df['engineTime']
            df['avgConsumed'] = df['mileage']/df['consumed']
            df.reset_index(inplace=True)
        elif period == 6 or period == 5 or period == 4 or period == 3:
            df = df.groupby(['year', 'month', 'date', 'nm', 'turn']).sum()
            df['ratio'] = df['consumed']/df['engineTime']
            df['avgConsumed'] = df['mileage']/df['consumed']
            df.reset_index(inplace=True)
            if (period == 3):
                df = df[df['date'] >= now - timedelta(days=7)]
            elif (period == 4):
                df = df[df['date'] >= now - timedelta(days=14)]
                df = df[df['date'] < now - timedelta(days=7)]
            elif (period == 5):
                df = df[df['date'] >= now - timedelta(days=30)]
            elif (period == 6):
                df = df[df['date'] >= now - timedelta(days=60)]
                df = df[df['date'] < now - timedelta(days=30)]
        elif period == 2 or period == 1:
            df['ratio'] = df['consumed']/df['produced']
            df['ratio'] = df['ratio'].fillna(0)
            if (period == 1):
                df = df[df['date'] >= now]
            elif (period == 2):
                df = df[df['date'] >= now - timedelta(days=1)]
    elif (option == 'pattern'):
        if pattern == 1:
            df = df.groupby(['nm', 'turn', 'nrohour']).mean()
            df['ratio'] = df['consumed']/df['engineTime']
            df['avgConsumed'] = df['mileage']/df['consumed']
            df.reset_index(inplace=True)
        elif pattern == 2:
            df = df.groupby(['nm', 'nroday', 'date']).sum()
            df['ratio'] = df['consumed']/df['engineTime']
            df['avgConsumed'] = df['mileage']/df['consumed']
            df.reset_index(inplace=True)
            df = df.groupby(['nm', 'nroday']).mean()
            df.reset_index(inplace=True)
    # filtramos por unidad
    df = df[df['nm'] == unit]
    df1 = df1.groupby(['nm', 'turn']).sum()
    df1.reset_index(inplace=True)

    idx = ['Chancado_I', 'Chancado_II']
    df_trip = trip[trip['tripTo'].isin(idx)]
    df_trip = df_trip.query('consumed < 100').query('consumed > 5')
    # sort df_trips by consumed
    df_trip = df_trip.sort_values(by=['consumed'], ascending=False)
    df_trip = df_trip.groupby(['trip', 'nm']).mean()

    data = df.to_dict('records')
    total = df1.to_dict('records')
    return jsonify({'data': data, 'total': total})
    
@app.route('/api/v1/position', methods=['GET'])
def ubication():
    df = position()
    data = df.to_dict('records')
    return jsonify({'data': data})

@app.route('/api/v1/realtime', methods=['GET'])
def realtime():
    #  enviar realtime los parametros totales de df
    total = pd.read_csv('{}/hour.csv'.format(path))
    total = total.groupby(['nm', 'turn']).sum()
    total.reset_index(inplace=True)
    # desde ahora 10 segundos atras se actualiza la ingomracion por hora avanzada
    end = datetime.now()
    arr = []
    # se calcula el timpo de tpal restante desde la ultima vez de total hasta hoy
    for unit in units['items']:
        start = total.query('nm == @unit["nm"]')['datetime'].max()
        try:
            _df = reportByHour(unit['id'], start, end)
            _df['nm'] = unit['nm']
            arr.extend(_df.to_dict('records'))
        except:
            print('error')
    trip = []
    for unit in units['items']:
        try:
            _df = reportGeofence(unit['id'], start, end)
            _df['nm'] = unit['nm']
            trip.extend(_df.to_dict('records'))
        except:
            print('error')
    return jsonify({'trip': trip, 'total': total})

@app.route('/api/v1/unit', methods=['GET'])
def unit():
    return jsonify(units)

@app.route('/api/v1/initialReport', methods=['GET'])
def initialReport():
    # lectura de report.csv usando path
    df = pd.read_csv('{}/report.csv'.format(path))
    arr = df.to_dict('records')
    return jsonify({'data': arr})

@app.route('/api/v1/report', methods=['GET'])
def report():
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
    arr = []
    for unit in units['items']:
        try:
            _df = reportByHour(unit['id'], start, end)
            _df['nm'] = unit['nm']
            arr.extend(_df.to_dict('records'))
        except:
            print('error')
    df = pd.DataFrame(arr)
    df.to_csv('{}/report.csv'.format(path), index=False)
    return jsonify({'data': arr})

@app.route('/api/v1/geofence/<int:id>', methods=['GET'])
def geofence(id):
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.now()
    df = reportGeofence(id, start, end)
    data = df.tail(8).iloc[::-1].to_dict('records')
    return jsonify({'data': data})

@app.route('/api/v1/initialAnalysis', methods=['GET'])
def initialAnalysis():
    df = pd.read_csv('./run/data/day.csv')
    df['year'] = df.apply(lambda x: 2023 if ((x['week'] == 53) and (x['year'] == 2022)) else x['year'], axis=1)
    df['week'] = df['week'].replace(53, 1)
    df['date'] = pd.to_datetime(df['date'])
    week = datetime.now().isocalendar()[1]
    weekday = datetime.now().weekday()
    week = weekday > 4 and week + 1 or week
    data = df[['mileage', 'avgSpeed', 'consumed', 'turn', 'date', 'week', 'nm', 'day', 'weekday', 'month', 'year']].query('nm == "HT61"').query('year == 2023').query('week == @week').to_dict('records')
    return jsonify({'data': data})

@app.route('/api/v1/analysis', methods=['GET'])
def analysis():
    id = request.args.get('id')
    range = request.args.get('range', default=None, type=int)
    axis = request.args.get('axis')
    print(id, range, axis)
    df = pd.read_csv('./run/data/day.csv')
    # se rectiicca el ano de la semana 53 por ser criterio de la mina, convirtiendo anos de 2022 a 2023 y cambinado semana 53 a 1
    df['year'] = df.apply(lambda x: 2023 if ((x['week'] == 53) and (x['year'] == 2022)) else x['year'], axis=1)
    df['week'] = df['week'].replace(53, 1)
    df['date'] = pd.to_datetime(df['date'])
    # number week of today
    if (axis == 'd'):
        week = datetime.now().isocalendar()[1]
        weekday = datetime.now().weekday()
        week = weekday > 4 and week + 1 or week
        range = week - range
        data = df[['mileage', 'avgSpeed', 'consumed', 'turn', 'date', 'week', 'nm', 'day', 'weekday', 'month', 'year']].query('nm == @id').query('year == 2023').query('week > @range').to_dict('records')
    elif (axis == 'w'):
        print('week')
        df1 = df.query('nm == @id')
        df1 = df1[['mileage', 'engineTime', 'moveTime', 'consumed', 'year', 'week', 'turn']].groupby(['year','week', 'turn']).sum()
        df1.reset_index(inplace=True)
        data = df1.tail(range).to_dict('records')
    elif (axis == 'm'):
        print('month')
    return jsonify({'data': data})

@app.route('/api/v1/trip', methods=['GET'])
def trip():
    id = request.args.get('id', default=None, type=int)
    start = request.args.get('start', default=None, type=int)
    end = request.args.get('end', default=None, type=int)
    print(id, start, end)
    df_trip = pd.read_csv('./run/data/trip.csv')
    _df = df_trip[['trip', 'tripFrom', 'tripTo', 'consumed', 'mileage', 'duration', 'avgSpeed', 'maxSpeed']].groupby(['trip', 'tripFrom', 'tripTo']).mean()
    _df.reset_index(inplace=True)
    trips = _df.to_dict('records')
    df = sensorTracing(id, start, end)
    df['llegada'] = df['coordinates'].shift(-1)
    df = df.drop(df.index[-1])
    data = df.to_dict('records')
    return jsonify({
            'data': data,
            'trips': trips
        })

if (__name__ == "__main__"):
    app.run(debug=True)

# set all columns
# pd.set_option('display.max_columns', None)

#  set all rows
# pd.set_option('display.max_rows', None)