import os
import datetime
import itertools
import socket
import sys

from dateutil import parser
import elasticsearch_helper as helper
from elasticsearch_helper import bulk_helper
from elasticsearch_helper import index_helper


class Mapping(object):
    def __init__(self, key, type):
        self.key = key
        self.type = type
        self.parse = self._get_parser(type)

    def _get_parser(self, type):
        calc_type = 'direct'
        if ':' in type:
            type, _, calc_type = type.partition(':')
        if calc_type == 'delta':
            # delta
            if type in ['integer', 'long', 'float', 'double']:
                if type == 'integer':
                    converter = int
                if type == 'long':
                    converter = long
                if type == 'float':
                    converter = float
                if type == 'double':
                    converter = float

                def _(v, p, delta):
                    if p is None:
                        p = v
                    delta_time = delta.total_seconds()
                    if delta_time != 0:
                        return (
                            (converter(v) - converter(p)) / delta_time)
                    else:
                        return (
                            (converter(v) - converter(p)))
                return _
            if type == 'date':
                return lambda v, p, delta: (parser.parse(v) - (parser.parse(p) if p is not None else parser.parse(v))).total_seconds()  # noqa
            return lambda v, p, delta: v
        else:
            # direct
            if type == 'integer':
                return lambda v, p, delta: int(v)
            if type == 'long':
                return lambda v, p, delta: long(v)
            if type == 'float':
                return lambda v, p, delta: float(v)
            if type == 'double':
                return lambda v, p, delta: float(v)
            if type == 'date':
                return lambda v, p, delta: parser.parse(v) if v else v
            return lambda v, p, delta: v


def _parse_mapping_args(argv):
    mappings = []
    datetime_index = -1
    index = 0
    for kv in argv:
        if kv != 'skip':
            key, _, type = kv.partition('=')
            mappings.append(Mapping(key, type))
        else:
            mappings.append(Mapping('', 'skip'))
            if datetime_index < 0:
                datetime_index = index
        index += 1
    return mappings, datetime_index


def stream():
    index_name = sys.argv[1]
    doc_type = sys.argv[2]
    mappings, datetime_index = _parse_mapping_args(sys.argv[3:])

    types = set([m.type for m in mappings if m != 'skip'])

    es = helper.make_from_env()
    index_mapping = {
        m.key: m.type if ':' not in m.type else m.type.split(':')[0]
        for m in mappings if m.type != 'skip'}
    index_mapping['host'] = 'non_analyzed'
    if 'date' not in types:
        index_mapping['@time'] = 'date'

    index_helper.make_index(
        es, index_name, doc_type, **index_mapping)

    hostname = os.environ.get('ES_HOSTNAME', socket.gethostname())
    parameter_len = len(mappings)
    with bulk_helper.bulk(es) as putter:
        try:
            prev_values = []
            prev_date = None
            while True:
                line = raw_input()
                values = line.split(None, parameter_len)
                if datetime_index >= 0:
                    now = parser.parse(values[datetime_index])
                else:
                    now = datetime.datetime.utcnow()
                if prev_date is not None:
                    delta = now - prev_date
                else:
                    delta = datetime.timedelta()
                data = {
                    m.key if m and m.key else "data":
                    m.parse(v, p, delta) if m else v
                    for m, v, p in itertools.izip_longest(
                        mappings, values, prev_values)
                    if not m or m.type != "skip"}
                if 'date' not in types:
                    data['@time'] = now
                data['host'] = hostname
                putter(index_name, None, doc_type, data)
                prev_values = values
        except Exception:
            pass


def del_index():
    es = helper.make_from_env()
    for name in sys.argv:
        index_helper.delete_index(es, name)
