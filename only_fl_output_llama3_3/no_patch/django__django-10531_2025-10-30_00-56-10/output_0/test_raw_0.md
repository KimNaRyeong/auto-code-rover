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
        # Create a model
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        # Register the model with admin
        admin.site.register(MyModel)

        # Change the publication date for an object of that model
        obj = MyModel(pub_date="2022-01-01")
        obj.save()
        obj.pub_date = "2023-01-01"
        obj.save()

        # Get the history of changes
        history = obj.history.all()

        # Check if the history contains verbose names
        for change in history:
            assert any("date published" in str(c) for c in change.field_name), "Verbose name not found"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a model, registers it with the admin interface, makes some changes to an object of that model, and then checks if the history of those changes contains verbose names. If not, it prints the stack trace of the assertion error and exits with code 1.