Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    try:
        class MyModel(models.Model):
            content_type_resource_contract = models.ForeignKey(
                'django.contrib.contenttypes.ContentType',
                on_delete=models.CASCADE,
                blank=True,
                null=True,
            )
            resource_contract_id = models.PositiveIntegerField(blank=True, null=True)
            resource_contract = models.GenericForeignKey('content_type_resource_contract', 'resource_contract_id')

        class MyAdmin(admin.ModelAdmin):
            list_filter = ((('resource_contract', admin.EmptyFieldListFilter),))

        admin.site.register(MyModel, MyAdmin)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

    else:
        print("Issue not present")
        exit(0)


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
    django.setup()
    main()

```

This script sets up a simple Django project, defines the model and admin class that reproduces the issue, and then runs the code. If any exception is raised during execution, it prints the stack trace using the provided function and exits with code 1. Otherwise, it prints a success message and exits with code 0.

Please note that you need to have Django installed in your Python environment for this script to run correctly.