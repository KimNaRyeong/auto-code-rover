To create a standalone Python file `reproducer.py` that reproduces the specific issue with Django's `CREATE INDEX` SQL statement formatting, we will ensure to import necessary Django components and properly setup Django settings. This script will attempt to reproduce the conditions under which the described SQL formatting issues occur and verify the correctness of the produced SQL statements. 

We will use Django model definitions with specific index configurations to trigger the generation of `CREATE INDEX` statements, capturing the output via Django's schema editor mechanism. Upon detection of formatting discrepancies, the script will raise an `AssertionError`.

```python
import os
import django
from django.conf import settings
from django.db import models, connections
from django.db.models.indexes import Index

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

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            '__main__',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
    )
    django.setup()

class CustomModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = '__main__'
        indexes = [
            Index(fields=['-name'], name='idx_desc'),
            Index(fields=['name'], opclasses=['text_pattern_ops'], name='idx_asc_opclass')
        ]

def main():
    setup_django_environment()
    connection = connections['default']
    with connection.schema_editor() as editor:
        sql_statements = []
        editor.collect_sql = True

        # Simulate the model creation to capture SQL statements
        editor.create_model(CustomModel)
        sql_statements.extend(editor.collected_sql)

        # Check SQL for correct whitespace
        error_messages = []
        for statement in sql_statements:
            if 'CREATE INDEX' in statement:
                if '"name"DESC' in statement:
                    error_messages.append('Missing whitespace before DESC in CREATE INDEX statement.')
                if 'text_pattern_ops )' in statement:
                    error_messages.append('Extra whitespace before closing parenthesis in CREATE INDEX statement with opclasses.')

        if error_messages:
            for error_message in error_messages:
                print(error_message, file=sys.stderr)
            raise AssertionError("SQL formatting issues detected.")

        print("No SQL formatting issues detected.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
```

This script sets up a minimal Django environment, defines a custom model with specific indexing requirements that mimic the problematic scenarios, and inspects the generated SQL for formatting issues. Note that it directly checks for the presence of problematic SQL patterns described in the issues. If such patterns are detected, it prints relevant error messages and exits with an assertion error, using the provided `print_stacktrace` function for detailed error reporting.