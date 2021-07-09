import json

from jsonschema import ValidationError, validate


class RuleSchemaValidator:
    def __init__(self, schema_path):
        self.schema_path = schema_path
        self.schema = None

    def validate(self, data):
        if self.schema is None:
            self._load_schema()
        try:
            validate(instance=data, schema=self.schema)
            return {"status": "ok", "message": "validation successful"}
        except ValidationError as ex:
            return {"status": "error", "message": str(ex)}

    def _load_schema(self):
        with open(self.schema_path) as json_file:
            self.schema = json.load(json_file)
