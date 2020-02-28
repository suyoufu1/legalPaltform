import contextlib
import time

from elasticsearch import helpers


@contextlib.contextmanager
def bulk(es, count=1000, sec=60):

    def _(index, id, type, data):
        _.cache.append({
            '_index': index,
            '_id': id,
            '_type': type,
            '_source': data})
        if len(_.cache) > count or (time.time() - _.last_flush) > sec:
            _flush()

    def _flush():
        helpers.bulk(es, _.cache)
        _.cache = []
        _.last_flush = time.time()

    _.cache = []
    _.last_flush = time.time()
    yield _

    _flush()
