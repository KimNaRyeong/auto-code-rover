import os
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps

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

def create_models(apps, schema_editor):
    class Model1(models.Model):
        field1 = models.CharField(max_length=255)
        field2 = models.CharField(max_length=255)
        class Meta:
            unique_together = ('field1', 'field2')
            index_together = ('field1', 'field2')

    class Model2(models.Model):
        field3 = models.CharField(max_length=255)
        field4 = models.CharField(max_length=255)

def delete_index_together(schema_editor, apps):
    try:
        schema_editor.delete_index_together('model1', ('field1', 'field2'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
    else:
        print("Issue fixed")
        exit(0)

if __name__ == '__main__':
    try:
        from django.db import connection
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection).migrator
        recorder.create_model('model1')
        recorder.create_model('model2')
        delete_index_together(None, None)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
    else:
        print("Issue fixed")
        exit(0)
