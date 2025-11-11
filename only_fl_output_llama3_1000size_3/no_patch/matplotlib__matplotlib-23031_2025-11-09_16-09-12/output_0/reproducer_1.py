import matplotlib
from unittest import mock
import sys
import traceback

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    with open('test_rcparams.rc', 'w', encoding='UTF-32-BE') as f:
        f.write('timezone: UTC')
    rc = matplotlib.rc_params_from_file('test_rcparams.rc', True, False)
    assert rc.get('timezone') == 'UTC'
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
