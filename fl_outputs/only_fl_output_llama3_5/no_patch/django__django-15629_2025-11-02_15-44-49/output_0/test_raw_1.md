Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models.signals import post_migrate
from django.db.migrations.operations.base import Operation

def db_collation_operation(db_collation):
    class DbCollationOperation(Operation):
        def __init__(self, model_name, db_collation):
            self.model_name = model_name
            self.db_collation = db_collation

        def database_state(self, schema_editor, of_type):
            if of_type == 'model':
                model = models.get_model(self.model_name)
                for field in model._meta.get_fields():
                    if isinstance(field, models.CharField) and field.primary_key:
                        field.db_collation = self.db_collation
            return

        def state_forwards(self, app_label, state):
            pass

    return DbCollationOperation

def apply_db_collation(model_name, db_collation):
    operation = db_collation_operation(db_collation)
    post_migrate.connect(lambda sender, **kwargs: operation(model_name, db_collation), sender=None)

class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=22, db_index=True, db_collation='utf8_bin')
    class Meta:
        managed = False

class Address(models.Model):
    id = models.CharField(primary_key=True, max_length=22, db_index=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=22, db_index=True)
    account = models.ForeignKey('Account', null=True, blank=True, on_delete=models.CASCADE)

if __name__ == '__main__':
    try:
        apply_db_collation('Account', 'utf8_bin')
        apply_db_collation('Address', 'utf8_bin')
        apply_db_collation('Profile', 'utf8_bin')
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present")
        exit(0)

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

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
    try:
        from django.conf import settings
        settings.configure()
        apply_db_collation('Account', 'utf8_bin')
        apply_db_collation('Address', 'utf8_bin')
        apply_db_collation('Profile', 'utf8_bin')
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present")
        exit(0)
```

This script will apply the `db_collation` to the models and then try to run makemigrations. If an error occurs, it will print the stack trace and raise an AssertionError.