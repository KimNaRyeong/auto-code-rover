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

def test_force_insert():
    from django.db import models

    class ParentModel(models.Model):
        id = models.BigIntegerField(primary_key=True)

    class ChildModel(ParentModel):
        pass

    try:
        child_model = ChildModel(id=1)
        child_model.save(force_insert=True)
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == '__main__':
    test_force_insert()
```

This script defines the `ParentModel` and `ChildModel`, creates an instance of `ChildModel`, and tries to save it with `force_insert=True`. If the issue is present, it will raise an `AssertionError`, print the stack trace using the provided function, and then re-raise the exception. If the issue is fixed, it will exit with code 0.