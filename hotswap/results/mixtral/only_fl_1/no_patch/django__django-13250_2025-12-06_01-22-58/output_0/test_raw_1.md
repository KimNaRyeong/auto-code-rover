 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import json
from django.core.exceptions import ValidationError
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class JSONField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "JSONField"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, str):
            return json.loads(value)
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

class Obj(models.Model):
    data = JSONField()

def create_objs():
    objs = [
        Obj(data={'a': 1, 'b': 2}),
        Obj(data={'a': 1, 'b': 3}),
        Obj(data={'a': 1, 'b': 2, 'c': {'a': 'b', 'c': 'd'}}),
        Obj(data={'k': True, 'l': False}),
        Obj(data={'d': ['e', {'f': 'g'}]}),
        Obj(data=[1, [2]]),
        Obj(data={'n': [None]}),
        Obj(data={'j': None}),
    ]
    for obj in objs:
        obj.full_clean()
        obj.save()
    return objs

def test_querying():
    objs = create_objs()
    for tests in [
            ({}, objs[2:5] + objs[6:8]),
            ({'baz': {'a': 'b', 'c': 'd'}}, [objs[7]]),
            ({'baz': {'a': 'b'}}, []),
            ({'baz': {'c': 'd'}}, []),
            ({'k': True, 'l': False}, [objs[6]]),
            ({'d': ['e', {'f': 'g'}]}, [objs[4]]),
            ({'d': ['e']}, []),
            ([1, [2]], [objs[5]]),
            ([1], []),
            ([2], []),
            ([3], []),
            ([4], []),
            ([5], []),
            ([6], []),
            ([7], []),
            ([8], []),
            ({'n': [None]}, [objs[4]]),
            ({'j': None}, [objs[4]]),
    ]:
        contained = Obj.objects.filter(**{f'data__contains': tests[0]})
        if contained != tests[1]:
            raise AssertionError(f"Expected {tests[1]}, but got {contained}")

if __name__ == "__main__":
    try:
        test_querying()
        print("No issue found.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
The script creates a `JSONField` model and populates it with