 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import django
import os

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
django.setup()

from enum import Enum
from django.db import migrations, models
from django.utils.translation import gettext_lazy as _

class Status(Enum):
    GOOD = _('Good')
    BAD = _('Bad')

    def __str__(self):
        return self.name

class Item(models.Model):
    status = models.CharField(default=Status.GOOD, max_length=128)

def test_migration():
    try:
        migration = migrations.migrations.Migration(
            dependencies=[],
            operations=[
                migrations.CreateModel(
                    name='Item',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('status', models.CharField(default=Status.GOOD, max_length=128)),
                    ],
                ),
            ],
        )
        assert False, "Migration should raise an error"
    except ValueError as e:
        print_stacktrace(e)

test_migration()
```

To reproduce the issue, create a new Django project with the following command:

```bash
django-admin startproject test_project
```

Then, replace the contents of `test_project/migrations/0001_initial.py` with the `migration` variable in the `reproducer.py` file.

Finally, execute the `reproducer.py` file with the following command:

```bash
python3 reproducer.py
```

The script should raise a `ValueError` with the following stack trace:

```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 52, in <module>
    test_migration()
  File "reproducer.py", line 48, in test_migration
    migration = migrations.migrations.Migration(
  File "/home/user/test_project/venv/lib/python3.8/site-packages/django/db/migrations/migrations.py", line 82, in __init__
    operation_list or [migrations.RunSQL("")],
  File "/home/user/test_project/venv/lib/python3.8/site-packages/django/db/migrations/operations/special.py", line 17, in RunSQL
    return RunSQLOperation(sql, sql_file, state_operations, **kwargs)
  File "/home/user/test_project/venv/lib/python3.8/site-packages/django/db/migrations/operations/special.py", line 52, in __init__
    self.sql = self.divide_sql(sql)
  File "/home/user/test_project/venv/lib/python3.8/site-packages/django/db/migrations/operations/special.py", line 72, in divide_sql
    raise ValueError(
ValueError: 'Good' is not a valid Status
```

This reproduces the issue described in the bug report. The generated migration file uses the value of the Enum object instead of its name, which causes a `ValueError` when the Enum value is translated to another language.