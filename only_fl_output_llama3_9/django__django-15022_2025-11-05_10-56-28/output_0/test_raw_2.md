Here is the reproducer script:

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
    try:
        from django.conf import settings
    except Exception as e:
        print_stacktrace(e)
        raise

    admin.autodiscover()
    ClientAdmin = admin.ModelAdmin
    client_qs = Client.objects.all()

    search_query = "test"
    for word in search_query.split():
        client_qs = client_qs.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))

    try:
        with connection.cursor() as cursor:
            client_qs.query.sql
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by performing a search query on the `Client` model using the provided search query. If the issue is present, it will print the stack trace and raise an `AssertionError`.