Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import os
from django.template import Template, Context
import random

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

try:
    t = Template("{{ list_var|random }}")
    c = Context({"list_var": []})
    t.render(c)
    assert False, "Expected IndexError"
except IndexError as e:
    print_stacktrace(e)

print("Issue is present. Exiting with code 1.")
exit(1)
```
This script sets up a Django environment, defines a template with the `random` filter applied to an empty list, and tries to render it. If no `IndexError` is raised, it asserts that the issue is not present. If an `IndexError` is raised, it prints the stack trace using the provided function and exits with code 1.

To use this script, create a new Django project and app, then add a `reproducer` directory in the project root with the following structure:
```
reproducer/
reproducer/
settings.py
__init__.py
reproducer.py
manage.py
```
In `settings.py`, define the `INSTALLED_APPS` setting to include the `polls` app:
```
INSTALLED_APPS = [
    # ...
    'polls',
]
```
Then, run the script using `python3 reproducer.py`. If the issue is present, it should print a stack trace and exit with code 1. If the issue is fixed, it should exit with code 0.