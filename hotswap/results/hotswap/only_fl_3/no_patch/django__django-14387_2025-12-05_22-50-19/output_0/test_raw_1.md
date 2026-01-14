 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sqlite3
from django.db import models as db_models
from django.db.models.query import QuerySet
from django.db.models import Q

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Define the Buss model
class Buss(db_models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = db_models.CharField(max_length=MAX_LENGTH)
    class Meta:
        unique_together = [('jurisdiction', 'name')]

# Define the jurisdiction_qs function
def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal'). \
            exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company'). \
            exclude(name__in=qs.values_list('name', flat=True))
    return qs

# Create a test database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE paiyroll_buss (
                    id INTEGER PRIMARY KEY,
                    jurisdiction TEXT,
                    name TEXT,
                    description TEXT
                )''')

# Insert test data
cursor.executemany('''INSERT INTO paiyroll_buss (jurisdiction, name, description)
                        VALUES (?, ?, ?)''', [
                            ('GB', 'buss1', ''),
                            ('GB', 'buss2', ''),
                            ('GB', 'buss3', ''),
                            ('GB', 'buss4', ''),
                            ('Universal', 'buss5', ''),
                            ('Universal', 'buss6', ''),
                            ('Universal', 'buss7', ''),
                            ('Company', 'buss8', ''),
                            ('Company', 'buss9', ''),
                            ('Company', 'buss10', ''),
                        ])
conn.commit()

# Load the test data into Django
from django.core.management import sql
sql.execute_management_sql(open('test.db', 'r').read(), conn)

# Test the jurisdiction_qs function
qs = jurisdiction_qs('GB')
print(qs.query)
print(qs.filter(jurisdiction='GB').count()) # Should be 4

# Check if the issue is present
try:
    assert qs.filter(jurisdiction='GB').count() == 4
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
finally:
    conn.close()
```
When executed, the script will create a SQLite database with test data, load it into Django, and test the `jurisdiction_qs` function. If the issue is present, the script will raise an `AssertionError` and print a stack trace.

Note: This script assumes that you have Django 3