import types
import sys
import traceback
from django.conf import settings

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
    print(settings.foo, settings.baz)
    assert False, "The settings object should not allow non-uppercase settings."
except AssertionError:
    raise
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
