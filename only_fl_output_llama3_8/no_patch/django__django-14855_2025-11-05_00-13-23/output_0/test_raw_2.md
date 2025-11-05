Here is the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.test.utils import setup_test_environment
setup_test_environment()

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        from django.contrib.admin.helpers import get_admin_url
        remote_obj = 'parent'
        url_name = 'admin:myapp_child_change'
        url = reverse(url_name, args=[quote(remote_obj.pk)], current_app='custom-admin')
        print(f"Generated URL: {url}")
    except NoReverseMatch as e:
        print_stacktrace(e)
        raise AssertionError("Failed to generate URL")

if __name__ == "__main__":
    main()
```

This script should be run from the root directory of your project.