Given the feedback and aiming for a successful reproduction of the issue that exits with code 0 when the issue is confirmed (by failing as expected) and provides a clear stack trace in case of unexpected errors, the corrected Python file `reproducer.py` should look like this:

```python
"""
reproducer.py: Script to reproduce the reported Django model inheritance issue.
"""

import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured

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

# Django environment setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=[
        "__main__",  # Hack to allow Django to recognize this script as an app
    ],
    SECRET_KEY="not_very_secret_in_this_case",
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

class Document(models.Model):
    pass

try:
    class Picking(models.Model):
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
        origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

    class PickingFixed(models.Model):
        origin = models.OneToOneField(Document, related_name='picking_fixed', on_delete=models.PROTECT)
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

    assert False, "ImproperlyConfigured error was expected but not raised."
except ImproperlyConfigured as e:
    print("Expected error was caught. Test reproduces the issue successfully.")
    print_stacktrace(e)
    sys.exit(0)
except Exception as e:
    print("An unexpected error occurred.", file=sys.stderr)
    print_stacktrace(e)
    assert False, "Test failed due to an unexpected error."
```

This script aims to reproduce the behavior where Django raises an `ImproperlyConfigured` exception due to confusion about which `OneToOneField` should have `parent_link=True` in a multi-inheritance scenario involving OneToOne links to the same parent model. It explicitly includes a mechanism to handle expected vs. unexpected exceptions to demonstrate the script's ability to identify the described issue correctly or raise awareness of any other unintended behaviors triggered by the Django framework's internal mechanics.

To run this script:
- Make sure you have Django installed in your Python environment (`pip install Django` might be necessary if it's missing).
- Place the script in the root directory of your project.
- Execute it using `python3 reproducerer.py`.

The script should exit with code 0 when it reproduces the issue correctly, showing that the test has passed by catching the specifically expected error `ImproperlyConfigured`. If any other error occurs, it will print a detailed stack trace to help diagnose the problem, ensuring clarity in what went wrong during execution.