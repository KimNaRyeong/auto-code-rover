 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sqlite3
from django.db import models as db_models
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

class Buss(db_models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = db_models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def main():
    # Initialize the database
    conn = sqlite3.connect('test.db')
    from django.core.management import sql
    sql.sql_install(conn)
    from django.core.management import create_test_db
    create_test_db('test.db', ensure_tables=True)

    # Create some sample data
    Buss.objects.create(jurisdiction='GB', name='b1')
    Buss.objects.create(jurisdiction='GB', name='b2')
    Buss.objects.create(jurisdiction='GB', name='b3')
    Buss.objects.create(jurisdiction='Universal', name='b4')
    Buss.objects.create(jurisdiction='Universal', name='b5')
    Buss.objects.create(jurisdiction='Company', name='b6')
    Buss.objects.create(jurisdiction='Company', name='b7')

    # Check that the function works as expected
    assert Buss.objects.filter(jurisdiction='GB').count() == 3
    assert Buss.objects.filter(jurisdiction__in=['GB','Universal','Company']).count() == 7
    assert jurisdiction_qs('GB').count() == 5

    # Check that the issue occurs
    assert jurisdiction_qs('GB').filter(jurisdiction='GB').count() == 3
    # This should raise an AssertionError
    assert jurisdiction_qs('GB').filter(jurisdiction='GB').count() == 5

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
The script initializes a SQLite database, creates some sample data, and checks that the `jurisdiction_qs` function works as expected. It then checks that the issue occurs by filtering the queryset with the same jurisdiction as the original filter.

When executed with `python3 reproducer.py`, the script should print a stack trace and raise an `AssertionError`:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 68, in <