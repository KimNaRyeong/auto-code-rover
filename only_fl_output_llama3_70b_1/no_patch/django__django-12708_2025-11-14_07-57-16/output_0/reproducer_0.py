import os
import sys

from django.conf import settings
from django.db import migrations, models

settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['reproducer'],
)

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.IntegerField()),
                ('field2', models.IntegerField()),
            ],
            options={
                'unique_together': {('field1', 'field2')},
                'index_together': {('field1', 'field2')},
            },
        ),
    ]

class MigrationDeleteIndex(migrations.Migration):
    dependencies = [('reproducer', '0001_initial')]

    operations = [
        migrations.AlterModelOptions(
            name='mymodel',
            options={'unique_together': {('field1', 'field2')}},  # remove index_together
        ),
    ]

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
    with os.environ['DJANGO_SETTINGS_MODULE'] == 'reproducer.settings':
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")

print("Issue is fixed")
sys.exit(0)
