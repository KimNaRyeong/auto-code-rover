Here is the `reproducer.py` script to reproduce the issue:
```
import os
from django.core.management import setup_environ
from django.db.models import Q
from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'  # Replace with your project settings module

setup_environ(os.environ.get("DJANGO_SETTINGS_MODULE"))

def reproducer():
    try:
        q = '%00'
        users = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        users.count()
        print("Issue is fixed")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

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

if __name__ == "__main__":
    reproducer()
```
Replace `'your_project.settings'` with your actual project settings module.

Run the script using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, it will print "Issue is fixed" and exit with code 0.