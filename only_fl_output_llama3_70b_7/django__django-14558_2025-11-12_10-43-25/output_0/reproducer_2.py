import os
import sys
from django import setup
from django.conf import settings
from django.forms import Form, JSONField

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

settings.configure()
setup()

class JSONForm(Form):
    json_field = JSONField(required=False)

try:
    form = JSONForm({})
    form.as_p()
except TypeError as e:
    if str(e) == "the JSON object must be str, bytes or bytearray, not NoneType":
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    else:
        print_stacktrace(e)
        sys.exit(1)
else:
    sys.exit(0)
