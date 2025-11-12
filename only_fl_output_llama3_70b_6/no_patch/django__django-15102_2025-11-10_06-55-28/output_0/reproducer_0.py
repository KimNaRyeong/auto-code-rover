import os
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

# Create a new directory for the project
project_dir = "mysite"
os.mkdir(project_dir)

# Run django-admin.py startproject with PYTHONPATH set
cmd = ["PYTHONPATH=.", "./django/bin/django-admin.py", "startproject", project_dir]
try:
    subprocess.check_call(cmd, cwd=os.path.dirname(__file__))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present: startproject does not honor umask")

# Check the permissions of settings.py
settings_file = os.path.join(project_dir, "mysite", "settings.py")
st = os.stat(settings_file)
permissions = st.st_mode & 0o777
assert permissions != 0o644, "Issue is present: startproject does not honor umask"

print("Issue is fixed: startproject honors umask")
