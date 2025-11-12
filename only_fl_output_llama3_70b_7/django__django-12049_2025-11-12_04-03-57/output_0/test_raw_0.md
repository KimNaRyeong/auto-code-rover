Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.db import migrations, models
from django.test.utils import get_runner

settings.configure(
    DATABASES={
        'my_DB': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'my_database',
            'USER': 'my_user',
            'PASSWORD': 'my_password',
            'HOST': 'localhost',
            'PORT': 3306,
            'OPTIONS': {'init_command': "SET SESSION collation_connection = 'utf8mb4_unicode_ci';"},
        }
    },
    INSTALLED_APPS=['my_app'],
)

class City(models.Model):
    countrycode = models.ForeignKey('Country', on_delete=models.CASCADE)

class Country(models.Model):
    pass

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

try:
    # Create the database tables
    get_runner(settings).setup_test_environment()
    City.objects.create(countrycode=Country.objects.create())

    # Apply the migration that should fail
    migration = migrations.Migration('my_first_app', '0001')
    operation = migrations.AddField(
        model_name='city',
        name='countrycode',
        field=models.ForeignKey(db_column='countryCode', on_delete=models.CASCADE, to='my_DB.country'),
    )
    executor = migrations.Executor(migration, connection='my_DB')
    executor.apply_migration(operation)

    # This should raise an OperationalError
    assert False, "Migration did not fail as expected"
except Exception as e:
    print_stacktrace(e)
    if isinstance(e, django.db.utils.OperationalError) and 'Table \'city\' already exists' in str(e):
        print("Issue reproduced successfully")
        sys.exit(0)
    else:
        raise
```
This script sets up a Django project with a MySQL database using the `utf8mb4_unicode_ci` collation, which is case-insensitive. It then creates a model `City` with a foreign key to `Country`, and applies a migration that should fail due to the case-insensitive collation.

If the issue is reproduced, the script will print "Issue reproduced successfully" and exit with code 0. If the issue is fixed, the script will raise an `AssertionError`.