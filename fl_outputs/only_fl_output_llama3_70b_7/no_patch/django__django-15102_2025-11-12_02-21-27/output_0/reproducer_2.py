import os
import stat
import sys
import subprocess

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
    # Create a new project with django-admin.py startproject
    subprocess.run([sys.executable, '-m', 'django', 'startproject', 'mysite'])

    # Check the permissions of settings.py
    settings_file = 'mysite/mysite/settings.py'
    st = os.stat(settings_file)
    perms = st.st_mode & 0o777

    # If the permissions are not restrictive enough, raise an AssertionError
    if perms != 0o600:
        raise AssertionError(f"Expected permissions 0o600, got {perms:o}")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
