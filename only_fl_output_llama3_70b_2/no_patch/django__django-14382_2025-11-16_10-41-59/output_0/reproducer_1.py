import os
import sys
from django.core.management import utils

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

def main():
    app_dir = 'myapp/'
    try:
        utils.validate_name(os.path.basename(app_dir), 'directory')
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error occurred when creating an app with a trailing slash"

if __name__ == "__main__":
    main()
