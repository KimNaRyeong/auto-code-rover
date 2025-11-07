Here is the reproducer script:

```python
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
        from django.db import models
        class MyModel(models.Model):
            foo = models.ManyToManyField('Bar', through='Baz')

        admin.site.register(MyModel)
        admin.ModelAdmin.filter_horizontal()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up a Django model with a ManyToManyField and attempts to use filter_horizontal on it. If the issue is present, this should raise an AssertionError and print out the stack trace.