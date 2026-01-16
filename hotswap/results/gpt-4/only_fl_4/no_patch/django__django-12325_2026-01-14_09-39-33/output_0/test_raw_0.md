```python
# reproducer.py

import os
import sys
from django.core.management import execute_from_command_line
from django.core.exceptions import ImproperlyConfigured
from django.db import models

# Define the print_stacktrace function
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

# Setup minimal Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer_settings')
sys.argv = ["reproducer.py", "check"]

# Minimal settings required for Django setup
settings = {
    'DEBUG': True,
    'USE_I18N': False,
    'USE_L10N': False,
    'USE_TZ': False,
    'DATABASES': {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    'INSTALLED_APPS': ['__main__'],
    'ROOT_URLCONF': '__main__',
}

def main():
    try:
        # Define models inline to reproduce the issue
        class Document(models.Model):
            pass

        class Picking(Document):
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

        # Dynamically setting DJANGO_SETTINGS_MODULE content
        from django.conf import settings as dj_settings
        for setting, value in settings.items():
            setattr(dj_settings, setting, value)

        # Trigger Django setup
        execute_from_command_line(sys.argv)

        # Check if the model works without raising an exception
        assert issubclass(Picking, Document), "Picking should subclass Document."

        # If arrived here, the expected exception was not raised; the issue seems resolved
        print("No issue detected. The Picking model was initialized without errors.")

    except ImproperlyConfigured as e:
        print_stacktrace(e)
        assert False, "Detected the configuration issue."

if __name__ == "__main__":
    main()
```

This script dynamically sets up a minimal Django environment capable of triggering the described issue. It defines the models `Document` and `Picking` to test the configuration of `OneToOneField` fields with respect to the `parent_link=True` parameter and the declaration order sensitivity. The script expects to raise an `ImproperlyConfigured` exception if the issue exists, prints out the stack trace for diagnosis, and fails with an assertion. Conversely, if the models are correctly initialized (indicating the issue has been resolved or does not exist in the setup used), it exits with a success message.