Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

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
    try:
        # Set the DJANGO_SETTINGS_MODULE environment variable
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

        from django.conf import settings
        from django.contrib.admin.models import LogEntry

        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        admin.site.register(MyModel)

        obj = MyModel()
        obj.pub_date = "2022-01-01"
        obj.save()

        # Check if the history shows verbose name
        assert "Changed date published." in str(LogEntry.objects.all()[0].action_time), "History does not show verbose name."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable, imports settings and LogEntry from django.contrib.admin.models, creates a model with a verbose field name, registers it in the admin interface, changes the publication date for an object of that model, and checks if the history shows the verbose name. If the issue is present, it will print the stack trace and raise an `AssertionError`.