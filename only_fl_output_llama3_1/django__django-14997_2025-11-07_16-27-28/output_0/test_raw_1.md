Here is the reproducer script:

```python
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.models.expressions import F
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.operations.special import RunPython

def create_model_tag(apps, schema_editor):
    model = apps.get_model('myapp', 'Tag')
    if not model:
        return
    model._meta.constraints = [
        models.UniqueConstraint(
            name='unique_name_value',
            fields=['name', 'value']
        )
    ]

def remove_constraint(model):
    model._meta.constraints = []

def recreate_table(apps, schema_editor):
    model = apps.get_model('myapp', 'Tag')
    if not model:
        return
    try:
        schema_editor.alter_field(model, None, models.CharField(max_length=150))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error recreating table")

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

def main():
    try:
        from myapp.models import Tag
        recreate_table(None, DatabaseSchemaEditor())
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error recreating table")

if __name__ == "__main__":
    main()
```

This script should be saved in a file named `reproducer.py` and run with the command `python3 reproducer.py`.