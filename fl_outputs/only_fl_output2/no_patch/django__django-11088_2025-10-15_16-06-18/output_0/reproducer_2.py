"""
reproducer.py
-------------
This script aims to reproduce an issue related to Django's handling of BinaryField defaults
during certain migration operations.
"""

import os
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

def run_reproducer():
    from django.conf import settings
    from django.core.management import execute_from_command_line

    project_name = "temp_project"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            '__main__',  # allows the app containing model to be recognized
        ),
    )

    from django.db import migrations, models
    from django.apps import apps
    apps.populate(settings.INSTALLED_APPS)
    from django.db.migrations.recorder import MigrationRecorder

    class InitialMigration(migrations.Migration):

        initial = True

        dependencies = []

        operations = [
            migrations.CreateModel(
                name='TableOne',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('field1', models.BinaryField(default='')),
                ],
            ),
        ]

    class SecondaryMigration(migrations.Migration):

        dependencies = [
            ('', 'initial'),
        ]

        operations = [
            migrations.AlterField(
                model_name='TableOne',
                name='field1',
                field=models.BinaryField(default=b''),
            ),
        ]

    # Applying migrations
    try:
        migrate_from = InitialMigration('0001_initial', '__main__')
        migrate_from.apply(None, None)

        # Modify the setting directly to simulate changing the model field's default
        # and attempt to migrate backwards, which should raise the targeted error.
        migrate_to = SecondaryMigration('0002_secondary', '__main__')
        migrate_to.apply(None, None)

        # Undo the migrations to trigger the fault
        migrate_to.unapply(None, None)
        migrate_from.unapply(None, None)

        # If we reach this point without error, the issue didn't occur
        assert False, "Expected migration reversal to raise TypeError."
    except Exception as e:
        if "can't escape str to binary" in str(e):
            # Issue is reproduced
            print("Issue reproduced successfully.")
            sys.exit(0)
        else:
            print_stacktrace(e)
            # Issue wasn't reproduced as expected
            assert False, "An unexpected error occurred."


if __name__ == '__main__':
    try:
        run_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error if the assertion fails or any unexpected issue occurs
