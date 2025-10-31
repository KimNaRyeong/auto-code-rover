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

try:
    from django.db import transaction
    admin.site.register(None, None)  # Register an empty model to simulate the admin interface
    clients = Client.objects.all()
    query = "test query with multiple words"
    for word in query.split():
        clients = clients.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))
    assert len(connection.queries) > 5, "Issue not reproduced"
except Exception as e:
    print_stacktrace(e)
    raise
finally:
    if 'django' in locals():
        del django
```

This script should be placed in the root directory of your project and executed by `python3 reproducer.py`.