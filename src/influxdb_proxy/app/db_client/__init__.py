from influxdb import InfluxDBClient

from influxdb_proxy.app import app


client = InfluxDBClient(
    app.config['DB_HOST'],
    app.config['DB_PORT'],
    app.config['DB_USER'],
    app.config['DB_PASS']
)
db_name = app.config['DB_NAME']


def db_exists(database):
    return database in [db['name'] for db in client.get_list_database()]


if not db_exists(db_name):
    client.create_database(db_name)
    app.logger.debug('DB created: {}'.format(db_name))
else:
    app.logger.debug('Using db: {}'.format(db_name))
