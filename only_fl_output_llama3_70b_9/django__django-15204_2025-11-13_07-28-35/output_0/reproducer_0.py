import sys
from django import forms
from django.utils.dateparse import parse_duration

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

class DurationField(forms.DurationField):
    pass

try:
    field = DurationField()
    field.clean('P3(3D')
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    sys.exit(0)
