Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib.admin import widgets
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
            foo = models.ManyToManyField('Bar', through='Baz')

        admin.site.register(MyModel)

        class MyAdmin(admin.ModelAdmin):
            filter_horizontal = ('foo',)
            filter_vertical = ('foo',)

        admin.site.register(MyModel, MyAdmin)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a Django project and defines a model `MyModel` with a ManyToManyField that uses an intermediary model. It then registers the model with the admin site and tries to use filter_horizontal and filter_vertical on it. If the issue is present, this should raise an AssertionError and print out the stack trace.