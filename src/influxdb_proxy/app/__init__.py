from flask import Flask
from influxdb_proxy.app.logger import configure_logging

from .config import configure

app = Flask(__name__)
application = app  # gunicorn

configure(app)
configure_logging(app)


from influxdb_proxy.app.api import base
from influxdb_proxy.app.api import routes
