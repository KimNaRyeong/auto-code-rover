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
        # Create a model with verbose name
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        # Register the model in admin
        admin.site.register(MyModel)

        # Change the publication date for an object of that model
        obj = MyModel()
        obj.pub_date = "2022-01-01"
        obj.save()

        # Check if the history shows verbose name
        assert "Changed date published." in str(obj.history.all()[0].change_message), "History does not show verbose name."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script creates a model with a verbose field name, registers it in the admin interface, changes the publication date for an object of that model, and checks if the history shows the verbose name. If the issue is present, it will print the stack trace and raise an `AssertionError`.