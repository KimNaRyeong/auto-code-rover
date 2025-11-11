Here is the reproducer script:

```python
def main():
    try:
        from django.db import models
        from django.contrib import admin

        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        admin.site.register(MyModel)

        my_model = MyModel()
        my_model.save()

        # Check the history
        history = admin.ModelAdmin.history(request=None, model=MyModel)
        print(history)  # This should raise an AssertionError

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
    main()
```

This script will create a Django model with a field that has a verbose name, register the model in the admin site, and then change the value of that field. If the issue is present (i.e., the history does not show human-readable messages), it will print the stack trace and raise an `AssertionError`.