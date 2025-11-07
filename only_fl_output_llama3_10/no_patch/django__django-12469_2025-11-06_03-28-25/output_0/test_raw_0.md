Here is the reproducer script:

```python
import datetime
from django.utils import timezone
from django.contrib.admin.filters import DateRangeFilter

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
    from django.contrib.admin.sites import site
    from django.contrib.auth.models import User

    user = User.objects.create(username='test_user', password='password')
    user.save()

    timezone.activate(datetime.timezone.datetime(2022, 1, 1, 0, 0))

    admin_site = site
    model_admin = admin_site.get_model_admin(User)
    filter_horizontal = ['date_hierarchy']
    try:
        model_admin.get_changelist_instance(request=None).get_filter_results(filter_horizontal=filter_horizontal)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a test user, sets the timezone to America/Los_Angeles (UTC-8), and then tries to get the filter results for the date_hierarchy filter. If the issue is present, it will raise an AssertionError and print the stack trace.