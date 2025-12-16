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

# Create a new SQLite database
conn = sqlite3.connect(':memory:')

# Create the Buss table
Buss._meta.db_table = 'paiyroll_buss'
Buss.objects.create_table(conn)

# Insert some sample data
Buss.objects.bulk_create([
    Buss(jurisdiction='GB', name='b1'),
    Buss(jurisdiction='GB', name='b2'),
    Buss(jurisdiction='GB', name='b3'),
    Buss(jurisdiction='Universal', name='b4'),
    Buss(jurisdiction='Universal', name='b5'),
    Buss(jurisdiction='Company', name='b6'),
    Buss(jurisdiction='Company', name='b7'),
])

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

# Test the jurisdiction_qs function
jq = jurisdiction_qs('GB')
print(f"jq.count(): {jq.count()}")

# Test filtering the queryset
jq_filtered = jq.filter(jurisdiction='GB')
print(f"jq_filtered.count(): {jq_filtered.count()}")

# Check if the generated SQL is correct
expected_sql = """
SELECT "paiyroll_buss"."id", "paiyroll_buss"."jurisdiction", "paiyroll_buss"."name", "paiyroll_buss"."description" FROM "paiyroll_buss"
WHERE ("paiyroll_buss"."jurisdiction" = GB OR ("paiyroll_buss"."jurisdiction" = Universal AND NOT ("paiyroll_buss"."name" IN (SELECT U0."name" FROM "paiyroll_buss" U0 WHERE U0."jurisdiction" = GB))) OR ("paiyroll_buss"."jurisdiction" = Company AND NOT ("paiyroll_buss"."name" IN (SELECT V0."name" FROM "paiyroll_buss" V0 WHERE