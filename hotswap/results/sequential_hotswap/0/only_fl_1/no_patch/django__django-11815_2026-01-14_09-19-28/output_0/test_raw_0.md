Certainly! Here's a standalone python file `reproducer.py` designed to reproduce the issue you've described. This script simulates the Django migration process involving an enum that uses translated strings as its values. Please make sure you have Django installed in your environment or virtual environment where you run this script.

```python
# reproducer.py
from enum import Enum
import os
import sys
from django.conf import settings
from django.db import models, migrations
from django.core.management.commands.makemigrations import Command as MakeMigrationsCommand
from django.utils.translation import gettext_lazy as _

# Setup Django environment
settings.configure(
    INSTALLED_APPS=["__main__"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    LANGUAGE_CODE='en',
    USE_I18N=True,
)

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

class Status(Enum):
    GOOD = _('Good')  # 'Good' will be translated
    BAD = _('Bad')   # 'Bad' will be translated

    def __str__(self):
        return self.name

class Item(models.Model):
    status = models.CharField(default=Status.GOOD, max_length=128)

def check_migrations_use_enum_name():
    try:
        # Simulate makemigrations command
        command = MakeMigrationsCommand()
        command.stdout = sys.stdout
        command.stderr = sys.stderr
        command.use_stdout = True
        migrations = command.make_migrations(apps=[(app.label, app) for app in models.apps.get_app_configs()], check=True, include_header=False)
        
        for migration in migrations.values():
            for operation in migration.operations:
                if isinstance(operation, migrations.AddField):
                    if not isinstance(operation.field.default, Enum):
                        raise AssertionError("Migration does not use Enum object as default.")
                    expected_default = f"{operation.field.default.__class__.__name__}['{operation.field.default.name}']"
                    actual_default = operation.field.default
                    if expected_default != actual_default:
                        raise AssertionError(f"Migration field default should be '{expected_default}', got '{actual_default}' instead.")
                
        print("The issue could not be reproduced. Migration uses Enum name as expected.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        from django.apps import apps
        apps.populate(settings.INSTALLED_APPS)
        check_migrations_use_enum_name()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

Please note that this script tries to dynamically create a Django app, generate a migration file for a model using an Enum with translated values, and then assert whether the migration behaves as expected. If the Django migration system behaves correctly (i.e., using the Enum's name rather than its value in migrations), this could potentially pass, but with the current Django behavior described, it should raise an `AssertionError`. This script exits with code 0 only if the issue is fixed and raises an exception if not.