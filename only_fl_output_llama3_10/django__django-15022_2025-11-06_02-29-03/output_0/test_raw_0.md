Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db.models import Q
from yourapp.models import Client, ClientOffice  # replace 'yourapp' with your actual app name

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
    admin.autodiscover()
    django.setup()

    client_qs = Client.objects.all()
    search_query = 'test query'
    for word in search_query.split():
        client_qs = client_qs.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))

    try:
        client_qs.count()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script should be placed in the root directory of your project and executed by `python3 reproducer.py`. The script will attempt to reproduce the issue by creating a query that filters clients based on multiple search words. If the issue is present, it will print the stack trace and raise an `AssertionError`.