import ast
import datetime
import json

from flask import jsonify
from flask import request

from influxdb_proxy.app.api.base import json_response
from influxdb_proxy.app.api.parser import Parser
from influxdb_proxy.app.auth import auth
from influxdb_proxy.app import app
from influxdb_proxy.app.db_client import client


@app.route('/insert/<db>/<measurement>', methods=['POST'])
@auth.login_required
def insert_measurement(db, measurement):
    if request.headers['content-type'] != 'application/json' or (
        not request.data
    ):
        return json_response('Bad request', 400)

    data = json.loads(request.data)
    app.logger.debug("New post request")

    points = {
        "measurement": measurement,
        "fields": data['fields'],
        "tags": data['tags']
    }

    if data['time']:
        points['time'] = data.get('time', datetime.datetime.now())

    client.write_points(
        points=[points],
        time_precision='ms',
        database=db
    )
    return jsonify({'ok': 'true'}), 200


@app.route('/insert', methods=['POST'])
@auth.login_required
def insert():
    if request.headers['content-type'] != 'application/json' or (
        not request.data
    ):
        return json_response('Bad request', 400)

    app.logger.debug("New post request")
    points_dict = Parser().parse()
    points = []
    for field_values in points_dict['fields']:

        points.append({
            "measurement": points_dict["measurement"],
            "tags": points_dict["tags"],
            "fields": field_values,
            "time": points_dict.get("time", datetime.datetime.now())
        })

    client.write_points(
        points=points,
        time_precision='n',
        database=app.config['DB_NAME']
    )
    return jsonify({'ok': 'true'}), 200
