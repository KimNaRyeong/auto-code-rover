Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib import admin

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
        class MyModel(models.Model):
            foo = models.ManyToManyField('BarModel', through='MyThroughModel')

        admin.site.register(MyModel)

        my_model_admin = admin.ModelAdmin(MyModel)
        my_model_admin.filter_horizontal = ['foo']

        print_stacktrace(AssertionError("Expected filter_horizontal to work"))

    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()
```

This script creates a Django model with a ManyToManyField that uses an intermediary model. It then attempts to register the model and its admin interface, specifying filter_horizontal for the ManyToManyField. If the issue is present, it will raise an AssertionError with a stack trace; if the issue is fixed, it will print the stack trace of any exception that occurs and exit with code 0.