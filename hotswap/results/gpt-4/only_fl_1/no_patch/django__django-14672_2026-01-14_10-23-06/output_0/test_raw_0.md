```python
# reproducer.py
import os
import django
from django.db import models
from django.core.management import execute_from_command_line

# Create a simple Django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
django.setup()

# Define settings for Django to avoid creating additional files
class Settings:
    SECRET_KEY = 'a-very-secret-key'
    INSTALLED_APPS = ('__main__',)
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}

settings.configure(Settings)

# Define models
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

def check_issue():
    try:
        # Simulate `python manage.py check` command, which triggers system checks
        execute_from_command_line(['manage.py', 'check'])
    except Exception as e:
        # If an expected issue is encountered, print the stack trace
        print_stacktrace(e)
        # Verify the exception is what we expect (unhashable type: 'list')
        assert isinstance(e, TypeError) and str(e) == "unhashable type: 'list'", "Unexpected error"
        print("The issue is present.")
        exit(1)
    print("No issue detected.")
    exit(0)

if __name__ == '__main__':
    check_issue()
```