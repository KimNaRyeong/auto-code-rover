```python
import os
import django
from django.conf import settings
from django.db import models
from django.core.management.commands.migrate import Command as MigrateCommand

# Configure Django. Requires DJANGO_SETTINGS_MODULE to be unset to avoid conflicts.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=["__main__"],
    USE_TZ=True,
)

django.setup()

# Define a simple model for demonstration purposes.
class MyModel(models.Model):
    name = models.CharField(max_length=100)

# Run migrations to create the database schema.
MigrateCommand().execute()

# Populate the database
MyModel.objects.create(name='a')
MyModel.objects.create(name='b')
MyModel.objects.create(name='c')

# Demonstrate the issue
group1 = MyModel.objects.filter(name='a')
group2 = MyModel.objects.filter(name='b')
group3 = MyModel.objects.filter(name='c')
combined_group = group1.union(group2)
group_and = combined_group & group1
group_or = combined_group | group3

try:
    # Here we're making an assumption about the expected behavior.
    # We assert that the SQL queries should differ, which they currently do not.
    assert str(combined_group.query) != str(group_and.query), "AND operation did not affect the query."
    assert str(combined_group.query) != str(group_or.query), "OR operation did not affect the query."
except AssertionError as e:
    # If the assertion fails, print the custom stack trace and exit with an error.
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

    print_stacktrace(e)
    exit(1)  # Non-zero exit code to indicate failure

# If the script reaches this point without errors, the behaviour has changed
# and it might be considered as the issue being fixed.
print("The script completed successfully. The issue might be fixed.")
exit(0)
```