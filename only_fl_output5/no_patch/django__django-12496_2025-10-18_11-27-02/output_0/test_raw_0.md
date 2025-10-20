```python
# reproducer.py
import os
import django
from django.conf import settings
import uuid

def setup_django_env():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',),
        SECRET_KEY='dummy',
    )
    django.setup()

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

from django.db import models

class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

class Child(Parent):
    body = models.TextField()

def test_case():
    setup_django_env()
    
    from django.db import connection
    
    Child.objects.create(title='', body='')
    
    insert_queries = [q for q in connection.queries if q['sql'].startswith('INSERT')]
    update_queries = [q for q in connection.queries if q['sql'].startswith('UPDATE')]
    
    # Check if there's an UPDATE query that shouldn't exist
    assert not update_queries, "Extra UPDATE query found"

if __name__ == "__main__":
    try:
        test_case()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("No issue detected.")
        raise SystemExit(0)
```