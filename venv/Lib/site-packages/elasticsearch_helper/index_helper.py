class _Mapping(object):

    def __init__(self):
        self._properties = {}

    def non_analyzed(self, name):
        self._properties[name] = {
            "type": "string",
            "fields": {
                "raw": {
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        }

    def analyzed(self, name):
        self._properties[name] = {
            "type": "string",
        }

    string = analyzed

    def integer(self, name):
        self._properties[name] = {
            "type": "integer",
        }

    def float(self, name):
        self._properties[name] = {
            "type": "float",
        }

    def double(self, name):
        self._properties[name] = {
            "type": "double",
        }

    def long(self, name):
        self._properties[name] = {
            "type": "long",
        }

    def date(self, name):
        self._properties[name] = {
            "type": "date",
        }


def make_index(es, name, doc_type, **name_type_map):

    m = _Mapping()
    for k, v in name_type_map.items():
        if v == 'None':
            continue
        getattr(m, v)(k)

    m.non_analyzed('data')
    if not es.indices.exists(name):
        es.indices.create(index=name)
    es.indices.put_mapping(index=name, doc_type=doc_type, body={
        doc_type: {
            'properties': m._properties
        },

    })


def delete_index(es, name):

    if es.indices.exists(name):
        es.indices.delete(index=name)
