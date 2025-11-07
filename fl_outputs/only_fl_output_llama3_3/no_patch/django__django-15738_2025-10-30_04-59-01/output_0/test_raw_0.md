Here is the reproducer script:

```python
import os
import django
from django.core.management import execute_from_command_line
from django.db.models.signals import post_migrate
from django.db import connection

# Set up Django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
django.setup()

# Create models
from app.models import Authors, ProjectDataSet, DataSet, Project

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
    # Create initial migration
    execute_from_command_line(['python3', 'manage.py', 'makemigrations', '--empty', '-n', 'initial'])
    with open('app/migrations/0001_initial.py', 'w') as f:
        f.write("from django.db import migrations\n")
        f.write("class Migration(migrations.Migration):\n")
        f.write("    dependencies = [('app', '0000a_migrations')]  # This line is important for the issue to reproduce\n")
        f.write("    operations = [\n")
        f.write("        migrations.AddField(\n")
        f.write("            model='app.authors',\n")
        f.write("            name='project_data_set',\n")
        f.write("            field=models.ForeignKey(\n")
        f.write("                to='app.projectdataset',\n")
        f.write("                on_delete=models.PROTECT,\n")
        f.write("            ),\n")
        f.write("        ],\n")
        f.write("    )\n")

    # Migrate
    execute_from_command_line(['python3', 'manage.py', 'migrate'])

    # Change field to many-to-many
    with open('app/migrations/0002_alter_authors_project_data_set_fieldtype.py', 'w') as f:
        f.write("from django.db import migrations\n")
        f.write("class Migration(migrations.Migration):\n")
        f.write("    dependencies = [('app', '0001_initial')]  # This line is important for the issue to reproduce\n")
        f.write("    operations = [\n")
        f.write("        migrations.AlterField(\n")
        f.write("            model='app.authors',\n")
        f.write("            name='project_data_set',\n")
        f.write("            field=models.ManyToManyField(\n")
        f.write("                to='app.projectdataset',\n")
        f.write("            ),\n")
        f.write("        ],\n")
        f.write("    )\n")

    # Migrate again
    execute_from_command_line(['python3', 'manage.py', 'migrate'])

except AssertionError as e:
    print_stacktrace(e)
    raise

finally:
    connection.close()
    if os.path.exists('app/migrations/0001_initial.py'):
        os.remove('app/migrations/0001_initial.py')
    if os.path.exists('app/migrations/0002_alter_authors_project_data_set_fieldtype.py'):
        os.remove('app/migrations/0002_alter_authors_project_data_set_fieldtype.py')
```

This script creates the models, creates an initial migration, migrates the database, changes the field type from foreign key to many-to-many, and then tries to migrate again. If the issue is present, it raises an `AssertionError` with a stack trace.