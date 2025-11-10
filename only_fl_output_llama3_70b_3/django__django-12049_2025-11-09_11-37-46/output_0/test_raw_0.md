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
            'NAME': 'my_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3306,
            'OPTIONS': {'init_command': "SET SESSION collation_connection = 'utf8mb4_unicode_ci';"},
        },
    },
    INSTALLED_APPS=['my_app'],
)

class City(models.Model):
    countrycode = models.ForeignKey('Country', on_delete=models.CASCADE)

class Country(models.Model):
    pass

def create_migration():
    from django.db.migrations.writer import MigrationWriter
    writer = MigrationWriter("0001_initial")
    writer.write_initial()
    with open("my_app/migrations/0001_initial.py", "w") as f:
        f.write(writer.as_string())

def main():
    os.makedirs('my_app', exist_ok=True)
    os.makedirs('my_app/migrations', exist_ok=True)

    create_migration()

    try:
        runner = get_runner(settings)
        runner.setup_test_environment()
        runner.configure_database_settings('my_DB')
        from django.core.management.commands import migrate
        migrate.Command().handle_rollback(verbosity=0, targets=[('my_first_app', '0001_initial')])
        print("Migration applied successfully")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Migration failed"

if __name__ == "__main__":
    main()
```
This script creates a Django project with a single app `my_app` and a migration that adds a foreign key field to the `City` model. It then runs the migration using the `migrate` command.

If the issue is present, the script will raise an `AssertionError` when the migration fails due to the case-insensitive collation. The `print_stacktrace` function will print the stack trace of the exception, including line numbers and code context.

To run the script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.