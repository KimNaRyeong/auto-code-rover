import django
import os
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Replace the following lines with the actual settings of your Django project
sys.path.append("path/to/edemo")
os.environ["DJANGO_SETTINGS_MODULE"] = "edemo.settings"

# Initialize Django
try:
    django.setup()
except Exception as e:
    print_stacktrace(e)
    assert False, "Django environment setup failed"

# Rest of the code
# ...
