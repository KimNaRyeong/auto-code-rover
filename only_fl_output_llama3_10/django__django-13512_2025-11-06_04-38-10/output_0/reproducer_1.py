import json
from django.utils.safestring import mark_safe
from django.core.exceptions import AssertionError

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

try:
    admin_display = mark_safe(json.dumps('中国'))
    assert '中国' == admin_display, "Admin doesn't display properly unicode chars in JSONFields."
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
