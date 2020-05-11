#!flask/bin/python
from flask_script import Manager
from influxdb_proxy.app import app

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
