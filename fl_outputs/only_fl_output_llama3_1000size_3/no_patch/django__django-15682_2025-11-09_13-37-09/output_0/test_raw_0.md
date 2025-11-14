Here is the reproducer script:

```python
import django
from django.db.models import F, DateTimeField
from django.db import models

def main():
    class TemplateVersion(models.Model):
        published_at = models.DateTimeField(null=True)

    try:
        template_versions = TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=True))
        if [tv.published_at for tv in template_versions] != [
            None,
            datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
            datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>)
        ]:
            raise AssertionError("Expected nulls_first=True to put None first")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    try:
        template_versions = TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=True))
        if [tv.published_at for tv in template_versions] != [
            datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
            datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>),
            None
        ]:
            raise AssertionError("Expected nulls_last=True to put None last")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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

This script creates a simple Django model, and then uses that model to reproduce the issue. It checks if the expected output is produced when using `nulls_first=True` and `nulls_last=True`. If the expected output is not produced, it raises an `AssertionError`, which is caught by the script and prints a stack trace before exiting with code 1.