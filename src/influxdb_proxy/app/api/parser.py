import ast
import json

from flask import request

from influxdb_proxy.app import app


class Parser:

    def __init__(self):
        self._data = json.loads(request.data)
        self._rules = dict((
            key.strip(), value.strip()
        ) for param_string in app.config['REQUEST_PARSING_RULES'].split(
            ','
        ) for key, value in [param_string.split(':')])

    def _get_copy_data(self):
        value = dict()
        value.update(self._data)
        return value

    def parse(self):
        points_dict = {}
        for rule_key, rule_source in self._rules.items():

            value = self._get_copy_data()
            value_found = False

            for k_s in rule_source.split('.'):
                if isinstance(value, dict) and k_s in value:
                    value_found = True
                    try:
                        # parse json-like string
                        value = ast.literal_eval(value[k_s])
                    except (ValueError, TypeError, SyntaxError):
                        value = value[k_s]
                else:
                    break

            if value_found:
                # 'a.b.c.d' -> ['d', 'c', 'b', 'a']
                #           -> {'a': {'b': {'c': {'d': value } } } }

                keys = rule_key.split('.')
                result = {keys[-1]: value}
                for k in keys[::-1][1::]:
                    result = {k: result}
                points_dict = merge(result, points_dict)
        return points_dict


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value
    return destination
