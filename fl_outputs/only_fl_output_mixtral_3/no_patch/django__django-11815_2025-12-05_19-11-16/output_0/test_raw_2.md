 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import django
from django.db import migrations
from django.utils.translation import gettext_lazy as _

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Status(Enum):
    GOOD = _('Good')
    BAD = _('Bad')
    def __str__(self):
        return self.name

class Item(models.Model):
    status = models.CharField(default=Status.GOOD, max_length=128)

def test_migration():
    # Initialize Django
    settings = django.conf.settings
    settings._configure_logging = lambda: None
    settings._setup_local_time_zone()
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=['tests'],
        MIGRATION_MODULES={'tests': 'tests'},
        ROOT_URLCONF='tests.urls',
        LANGUAGE_CODE='en',
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )

    # Create migration
    migrations.create_model(
        name='Item',
        fields=[
            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('status', models.CharField(default=Status.GOOD, max_length=128)),
        ],
    )

    # Check the generated migration file
    migration_file = django.db.migrations.migration.Migration(__name__, '0001_initial')._operations[0]
    assert migration_file.field_type == 'CharField', "The field type should be CharField"
    assert migration_file.default == Status('Good'), "The default value should be the Status Enum object"
    assert migration_file.default_value == "'Good'", "The default value should be a string representation of the Status Enum value"
    assert migration_file.options == {'max_length': 128}, "The options should be {'max_length': 128}"

    # Raise an AssertionError if the issue is present
    assert migration_file.default == Status['GOOD'], "The default value should be the Status Enum name"

# Run the test
try:
    test_migration()
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The script initializes Django, creates a migration file for the `Item` model, and checks the generated migration file. If the default value of the `status` field is the `Status` Enum object instead of the Enum name, the script raises an `AssertionError` and prints a stack trace.

Note that the script uses an in-memory SQLite database for simplicity. You may need to modify the script to use a different database if you encounter any issues.