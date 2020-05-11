import os


ENV_PREFIX = 'APP__'


def _from_env(app):
    for key, default in [
        ('LOG_PATH', '/var/log'),
        ('DEBUG', False),
        ('AUTH_USER', ''),
        ('AUTH_PASS', ''),
        ('DB_HOST', '127.0.0.1'),
        ('DB_PORT', '8086'),
        ('DB_NAME', 'db0'),
        ('DB_USER', ''),
        ('DB_PASS', ''),
        ('REQUEST_PARSING_RULES', 'measurement:measurement,fields:fields,tags:tags'),
    ]:
        app.config[key] = os.getenv('{}{}'.format(ENV_PREFIX, key), default)


def configure(app):
    path = os.environ.get('INFLUXDB_PROXY_SETTINGS_PATH')
    app.config['JSON_AS_ASCII'] = False
    if path and os.path.exists(path):
        app.config.from_json(path)
    else:
        _from_env(app)
