import os

import elasticsearch


def make_from_env():
    return elasticsearch.Elasticsearch([
        os.environ.get('ES_HOST', 'localhost:9200')])
