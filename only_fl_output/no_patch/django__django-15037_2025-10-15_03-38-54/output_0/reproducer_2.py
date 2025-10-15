"""
reproducer.py

This script aims to reproduce an issue where Django's `inspectdb` command does not handle a foreign key to a specific field correctly.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

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

# Define a minimal settings configuration required for Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[],
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

# Prepare and execute SQL statements to create the tables with the described issue
def create_test_tables():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                other_id INTEGER UNIQUE
            );""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                other_id INTEGER,
                CONSTRAINT myconst FOREIGN KEY(other_id) REFERENCES foo(other_id)
            );""")

try:
    create_test_tables()

    # Redirect stdout to capture the output of inspectdb
    from io import StringIO
    out = StringIO()
    sys.stdout = out

    call_command('inspectdb')

    sys.stdout = sys.__stdout__  # Reset stdout
    output = out.getvalue()

    # Check the generated model does not reference foo.other_id
    if "ForeignKey(to='foo', to_field='other_id')" not in output:
        raise AssertionError("The issue is present: ForeignKey to 'foo(other_id)' not properly handled.")

    # Cleaning up
    os.remove('db.sqlite3')

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("The issue seems to have been fixed.")  # If the script reaches this point without errors
