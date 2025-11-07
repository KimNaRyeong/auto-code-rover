Below is a standalone python script named `reproducer.py`. This script is written with the intention to reproduce the described issue related to the `CREATE INDEX` statement formatting in Django models. When executed, it will check for the specific formatting issues as described in your request and raise an `AssertionError` if the described issue is present, printing a detailed stack trace of the issue location.

Please note, you need to have Django installed and a Django project setup to use this script directly, as it relies on Django's ORM (Object-Relational Mapping) to define models and attempt to create an index with the specifics described.

```python
# reproducer.py
import django
from django.conf import settings
from django.db import models
from django.db.backends.ddl_references import IndexName

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )
    django.setup()

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

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
    setup_django_environment()

    # Attempt to create an index with and without opclasses and check the SQL statement generated
    discrepancy_found = False
    index_no_opclass = models.Index(fields=['-name'], name='index_no_opclass')
    index_with_opclass = models.Index(fields=['name'], name='index_with_opclass', opclasses=['text_pattern_ops'])

    # Mock model to simulate SQL generation
    model = Author

    # Generate SQL for index without opclass
    statement_no_opclass = index_no_opclass.create_sql(model, schema_editor=None)
    
    # Expected SQL format: CREATE INDEX "idx" ON "schema_author" ("name" DESC)
    if 'DESC)' in str(statement_no_opclass):
        print("Issue reproducer: Incorrect spacing in CREATE INDEX statement without opclass.")
        discrepancy_found = True

    # Generate SQL for index with opclass
    statement_with_opclass = index_with_opclass.create_sql(model, schema_editor=None)
    
    # Expected SQL format: CREATE INDEX "idx" ON "schema_author" ("name" text_pattern_ops)
    if ' text_pattern_ops )' in str(statement_with_opclass):
        print("Issue reproducer: Incorrect spacing in CREATE INDEX statement with opclass.")
        discrepancy_found = True

    if discrepancy_found:
        raise AssertionError("CREATE INDEX statement formatting issue detected.")

if __name__ == '__main__':
    try:
        main()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
```

To use this script effectively:

1. Ensure Django is installed in your environment. You can install Django using pip if not already installed:
   ```
   pip install django
   ```

2. Run this script from the root directory of your Django project using:
   ```
   python3 reproducer.py
   ```

The script setups a minimal Django environment, defines a model, attempts to create two kinds of indices (with and without opclass), and checks the resulting SQL statements for the described spacing issue. If the issue is present, it will raise an `AssertionError` and print a detailed stack trace.