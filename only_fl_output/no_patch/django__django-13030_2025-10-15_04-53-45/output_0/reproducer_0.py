# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line


# Minimal Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testdb.sqlite3',
        },
    },
    INSTALLED_APPS=('example.core',),
    ROOT_URLCONF='',
)

# Define models in an "example.core" app
os.makedirs('example/core/migrations', exist_ok=True)
with open('example/core/__init__.py', 'w') as f:
    f.write('')
with open('example/core/models.py', 'w') as f:
    f.write('''
from django.db import models

class Author(models.Model):
    pass

class Book(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.DO_NOTHING)
''')

with open('example/core/migrations/__init__.py', 'w') as f:
    f.write('')

# Setup Django
django.setup()
execute_from_command_line(['manage.py', 'makemigrations', 'core'])
execute_from_command_line(['manage.py', 'migrate'])

# Import inside function to avoid AppRegistryNotReady exception
from example.core.models import Author, Book
from django.db import connection


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


def test_query_without_null():
    try:
        a1 = Author.objects.create()
        Book.objects.create(author=a1)
        Book.objects.create(author=None)
        Book.objects.prefetch_related('author')
        assert all('NULL' not in query['sql'] for query in connection.queries), "Query includes NULL in IN clause"
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    try:
        test_query_without_null()
    except AssertionError:
        exit(1)
    else:
        print("Issue fixed or not present.")
        exit(0)
