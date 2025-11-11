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
    from django.db import models
    from django.apps import apps

    class BaseApp(models.Model):
        class Meta:
            db_table = 'table_name'

    class App1(models.Model):
        class Meta:
            app_label = 'app1'
            db_table = 'table_name'

    class App2(models.Model):
        class Meta:
            app_label = 'app2'
            db_table = 'table_name'

    try:
        apps.ready()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
```

This script creates three models, `BaseApp`, `App1`, and `App2`, each with the same table name. When you run this script with Django 2.2 or later, it should print the stack trace of the ProgrammingError and raise an AssertionError.