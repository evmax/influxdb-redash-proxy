# Webhook proxy for InfluxDb and Redash

Proxies post requests from `redash` (https://github.com/getredash/redash) to `influxdb` (https://www.influxdata.com/)

## For development

### Setup

Install python3, pip3, virtulenv.
Create virtualenv and install requirements

```
$ pip install -r ./requirements/dev.txt
```

### Development run

activate environment
```
$ workon my_env
```
copy and edit config file
```
$ cp ./config.json.sample /path/to/config.json
$ export INFLUXDB_PROXY_SETTINGS_PATH=/path/to/config.json
$ cd ./src/
$ python manage.py runserver -p 5052
```

### Request
Check alive
```
$ curl -X GET http://127.0.0.1:5052/health-check
```

#### Post request
Use Basic auth for authorization

Use `/insert/db/measurenment` for raw insert
```
$ curl -X POST http://127.0.0.1:5052/insert/db_name/measurement_name -H 'Authorization: Basic base64ForUserPass' -d '{"some_param": "some_value"}'
```

Use `/insert` to post using parsing rules to specified db (see `REQUEST_PARSING_RULES` and db params in `config.json`)
```
$ curl -X POST http://127.0.0.1:5052/insert -H 'Authorization: Basic base64ForUserPass' -d '{"youSpecialJson": {"measurement": "some_value"}}'
```

## With docker
Build
```
$ docker build -t influxdb_proxy:latest .
```
or
```
docker-compose pull
```
check params in `./docker/.env`, and
```
$ docker-compose up
```
