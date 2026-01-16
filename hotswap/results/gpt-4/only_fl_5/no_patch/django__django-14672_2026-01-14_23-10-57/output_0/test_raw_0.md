```python
# reproducer.py

from django.db import models
from django.core.management import call_command
from django.conf import settings


# Setting up minimal Django settings required for the test
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script is the main Django app
    ],
    USE_TZ=True,
)

# Define the models according to the issue description
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
    try:
        from django.core.management import execute_from_command_line

        # Mimic running the "check" command which should trigger the error
        execute_from_command_line(['manage.py', 'check'])

        # If no error occurs, we assume the issue has been fixed and exit normally
        print("No issue detected.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Assert the specific error to ensure we're detecting the issue correctly
        assert "unhashable type: 'list'" in str(e), "The detected exception does not match the expected issue."
        exit(1)
```