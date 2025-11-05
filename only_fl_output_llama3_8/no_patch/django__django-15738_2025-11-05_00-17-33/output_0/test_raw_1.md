Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError
from django.core.management.commands.makemigrations import CommandError
from django.core.exceptions import ValidationError
from django.core.management import call_command

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

django.setup()

from app.models import Authors, ProjectDataSet, DataSet, Project

try:
    # Create the models
    Authors.objects.create(project_data_set=ProjectDataSet.objects.create(data_set=DataSet.objects.create(name='test'), project=Project.objects.create(name='test')),
                            state=1, start_date='2022-01-01')

    # Change the field from foreign key to many to many
    Authors._meta.get_field('project_data_set').remote_field = models.ManyToManyField(ProjectDataSet)

    # Try to make migrations
    call_command('makemigrations', 'app')
    call_command('migrate')

except (IntegrityError, CommandError, ValidationError) as e:
    print_stacktrace(e)
    exit(1)
```

This script creates the models and data, changes the field from foreign key to many to many, and then tries to make migrations. If any error occurs during this process, it will be caught and printed with a stack trace.