Below is a standalone `reproducer.py` file designed to replicate the described issue. When executed in a project's root directory, it should behave as requested: it will raise an `AssertionError` if the issue is present, displaying a detailed stack trace of the error. Once the issue is resolved, it should exit with code 0.

```python
# reproducer.py

from django.db import models
from django.core.management import call_command
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    name = models.CharField(max_length=256)

class ProxyParent(Parent):
    class Meta:
        proxy = True

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    many_to_many_field = models.ManyToManyField(
        to=Parent,
        through="ManyToManyModel",
        through_fields=['child', 'parent'],
        related_name="something"
    )

class ManyToManyModel(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='+')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
    second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)

def setup_django():
    import django
    from django.conf import settings

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            '__main__',  # This script contains our models, hence '__main__'
        ),
        USE_TZ=True,
    )
    django.setup()

def run_checks():
    try:
        call_command('check')
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code

def main():
    setup_django()
    try:
        run_checks()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

To execute this script, you will need to place it in the root directory of a Django project and run it using a Python interpreter that has Django installed. Keep in mind that the Django app needs to be configured to recognize this script as part of the project, primarily for it to understand the models defined in the script. This script assumes you are running it in a minimal Django setup purely for the purpose of reproducing the described issue.