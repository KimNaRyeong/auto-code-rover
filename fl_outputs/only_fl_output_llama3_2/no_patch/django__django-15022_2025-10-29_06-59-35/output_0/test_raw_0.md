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
    admin.site.register(Client, ClientAdmin)
    clients = Client.objects.all()
    query = 'test search query'
    for word in query.split():
        clients = clients.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))
    try:
        list(clients)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    reproduce_issue()
```

This script will create an admin site, register the `Client` model with the `ClientAdmin`, and then perform a search query that should trigger the unnecessary joins. If the issue is present, it will print the stack trace and raise an `AssertionError`.