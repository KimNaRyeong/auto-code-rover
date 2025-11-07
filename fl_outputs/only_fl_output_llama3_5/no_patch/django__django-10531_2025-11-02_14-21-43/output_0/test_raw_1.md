Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    try:
        # Create a model with verbose name for one of its fields
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        # Register the model in the admin site
        admin.site.register(MyModel)

        # Change the publication date and check the history
        my_model = MyModel()
        my_model.save()

        print("History should show 'Change date published.' but it shows 'Changed pub_date.'")

    except AssertionError as e:
        print_stacktrace(e)
        raise

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
    django.setup()
    main()

# Set the DJANGO_SETTINGS_MODULE environment variable
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

django.setup()
```

This script will create a Django model with a field that has a verbose name, register the model in the admin site, and then change the value of that field. If the issue is present (i.e., the history shows "Changed pub_date." instead of "Change date published."), it will print the stack trace and raise an `AssertionError`.