import json


class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "json_repr"):
            return o.json_repr()
        return json.JSONEncoder.default(self, o)
