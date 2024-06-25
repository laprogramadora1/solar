from marshmallow import fields, Schema, validate

not_blank = validate.Length(min=1, error='Campo vacio')

class Trim(fields.Field):
    def __init__(self, inner, *args, **kwargs):
        self.inner = inner
        super().__init__(*args, **kwargs)

    def _bind_to_schema(self, field_name, parent):
        super()._bind_to_schema(field_name, parent)
        self.inner._bind_to_schema(field_name, parent)

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'strip'):
            value = value.strip()
        return self.inner._deserialize(value, *args, **kwargs)

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)