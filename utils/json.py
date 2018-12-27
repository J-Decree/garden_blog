import json
from datetime import datetime, date
from responsitory.Models.web import *


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return {k: json.dumps(v, cls=CJsonEncoder) for k, v in obj.__dict__.items()}
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    pass
