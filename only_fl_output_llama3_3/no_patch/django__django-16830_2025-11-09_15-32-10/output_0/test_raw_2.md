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
    from django.conf import settings

    settings.configure()

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

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before importing Django models. This should allow the script to reproduce the issue.