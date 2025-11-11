import os
from django.db import models
from django.core.management import call_command
from django.core.exceptions import AssertionError

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

def reproduce_issue():
    try:
        models.get_model('bar')
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from django.conf import settings
    settings.configure()

    class Foo(models.Model):
        id = models.AutoField(primary_key=True)
        other_id = models.IntegerField(unique=True)

    class Bar(models.Model):
        id = models.AutoField(primary_key=True)
        other_id = models.IntegerField()
        myconst = models.ForeignKey(Foo, to_field='other_id', on_delete=models.CASCADE)

    call_command('inspectdb', 'bar')

    reproduce_issue()

    print("Issue reproduced successfully.")
    exit(0)
