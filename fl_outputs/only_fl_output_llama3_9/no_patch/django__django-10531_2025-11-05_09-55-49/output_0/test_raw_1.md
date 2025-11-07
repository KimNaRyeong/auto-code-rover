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
        django.setup()
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        admin.site.register(MyModel)

        my_model = MyModel()
        my_model.pub_date = '2022-01-01'
        my_model.save()

        my_model.pub_date = '2022-02-01'
        my_model.save()

        history = my_model.history
        if not all([msg.startswith('Changed date published.') for msg in history]):
            raise AssertionError("Expected verbose name in model history")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up Django before creating the model and registering it with the admin site. It then saves two versions of the model, checks if the history messages contain the verbose name "date published", and raises an `AssertionError` if not.