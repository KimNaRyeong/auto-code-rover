import os
import stat
import sys

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

# Set umask to 077
os.umask(0o77)

try:
    # Create a new project using django-admin.py
    from django.core.management import execute_from_command_line
    args = ['django-admin.py', 'startproject', 'mysite']
    execute_from_command_line(args)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("startproject failed with permission denied error")

# Check the permissions of settings.py
settings_file = "mysite/mysite/settings.py"
st = os.stat(settings_file)
permissions = st.st_mode & 0o777

if permissions != 0o600:  # expected permissions with umask 077
    raise AssertionError(f"Expected permissions 0o600, got {permissions:o}")
else:
    print("Issue not present")
    sys.exit(0)
