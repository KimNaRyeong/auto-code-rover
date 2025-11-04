Here is the reproducer script:

```python
from django.db import models
from django.db.models.signals import post_migrate
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import StateApps

def db_collation_operation(apps, schema_editor):
    model = apps.get_model('myapp', 'Account')
    model._meta.db_table = 'b_manage_account'
    model._meta.db_collation = 'utf8_bin'

class DbCollationOperation(Operation):
    def __init__(self, model_name):
        self.model_name = model_name

    def database_state(self, apps_state, schema_editor):
        db_collation_operation(apps_state.apps, schema_editor)

    def state_forwards(self, app_label, schema_editor):
        pass

def create_models(apps, schema_editor):
    class Account(models.Model):
        id = models.CharField(max_length=22, primary_key=True, db_collation='utf8_bin', db_index=True)
        # ...

    class Address(models.Model):
        id = models.CharField(max_length=22, primary_key=True, db_collation='utf8_bin', db_index=True)
        account = models.OneToOneField('Account', on_delete=models.CASCADE)

    class Profile(models.Model):
        id = models.CharField(max_length=22, primary_key=True, db_collation='utf8_bin', db_index=True)
        account = models.ForeignKey('Account', verbose_name=_('account'), null=True, blank=True, on_delete=models.CASCADE)

def main():
    try:
        create_models(None, None)
        DbCollationOperation('myapp').run(None, None)
        post_migrate.send(sender='myapp')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error occurred")

if __name__ == '__main__':
    main()
```

This script creates the models with `db_collation` and then runs a migration to create the tables. The `post_migrate` signal is sent, which should trigger the creation of foreign key constraints. If an error occurs during this process, it prints the stack trace and raises an `AssertionError`.