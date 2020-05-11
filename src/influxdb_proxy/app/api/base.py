import uuid
from flask import jsonify
from flask import request

from influxdb_proxy.app import app


@app.before_request
def set_request_id():
    """Set request id for logging."""
    request.request_id = request.headers.get("x-request-id", uuid.uuid4().hex)


@app.route('/health-check', methods=['GET'])
def health():
    return jsonify({
        'result': 'alive'
    })


@app.errorhandler(404)
def custom_404(error):
    return json_response('Not found', 404)


@app.errorhandler(405)
def custom_405(error):
    return json_response('Method not allowed', 405)


def json_response(payload, status=200):
    return jsonify(payload), status, {'content-type': 'application/json'}
