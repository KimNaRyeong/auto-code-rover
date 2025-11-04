from django.db import models
from django.db.models.signals import post_migrate
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import StateApps
import os

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'
    from myapp.models import Account, Address, Profile
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
