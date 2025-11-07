import os
import sys
import django
from django.conf import settings
from django.db import migrations, models
from django.core.management import call_command

# Print stack trace helper function
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


MINIMAL_SETTINGS = {
    'INSTALLED_APPS': ['__main__'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
        }
    }
}

settings.configure(**MINIMAL_SETTINGS)
django.setup()


# Initial Migration
class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name='TableOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.BinaryField(default='')),
            ],
        ),
    ]


# Apply the migration
MIGRATION = Migration('0001_initial', '__main__')

try:
    executor = migrations.executor.MigrationExecutor(connection=django.db.connection)
    executor.apply_migration(executor.loader.project_state(), MIGRATION)

    # Simulate changing field default and making new migration
    MIGRATION.operations[0].fields[1] = ('field1', models.BinaryField(default=b''))
    executor.loader.build_graph()  # Rebuild the migration graph after changes
    executor.recorder.record_applied('__main__', '0002_modify_default')

    # Now, try to reverse to the initial state
    executor.migrate(targets=[('__main__', '0001_initial')])
    exit(0)  # If everything goes well, exit

except Exception as e:
    print_stacktrace(e)
    assert "can't escape" in str(e), "Issue not reproduced"
    exit(1)  # Exit with error if issue is present
