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

        # Create a model with verbose name
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        # Create an admin site and register the model
        admin.site.register(MyModel, verbose_name='My Model')

        # Change the publication date for an object of that model
        obj = MyModel()
        obj.pub_date = '2022-01-01'
        obj.save()

        # Check if the history shows human-readable messages
        assert "Changed date published." in str(obj.history.all()[1].change_message)

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable, which is required for Django to function properly. It then creates a model with a verbose name, registers it to an admin site, changes the publication date for an object of that model, and checks if the history shows human-readable messages. If the issue is present (i.e., the history does not show human-readable messages), the script will print the stack trace and exit with code 1.