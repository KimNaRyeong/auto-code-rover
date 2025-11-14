Here is a revised standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.contrib import admin
from django.db.models import Q
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

def reproduce_issue():
    django.setup()
    
    client_qs = Client.objects.all()
    for query in ["word1 word2", "word3 word4"]:
        query_qs = client_qs.filter(Q(name__icontains=query) | Q(name2__icontains=query) | Q(contact_person__icontains=query) | Q(clientoffice__name__icontains=query) | Q(clientoffice__name2__icontains=query))
        cursor = connection.cursor()
        cursor.execute("EXPLAIN (FORMAT JSON) %s" % query_qs.query.as_sql())
        result = cursor.fetchall()[0]['Plan']
        if 'Join' in result['Node Type']:
            raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a Django project, performs searches for clients using various query strings, and then checks the SQL query plan to see if any joins are present. If any joins are found, it raises an `AssertionError`, which is caught and printed to the console along with a stack trace.

To use this script, replace `'word1 word2'` and `'word3 word4'` in the loop with your actual search queries. Then, run the script using `python3 reproducer.py`. If the issue is present, you should see an `AssertionError` message followed by a stack trace.