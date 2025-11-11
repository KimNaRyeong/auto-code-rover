Here is the reproducer script:

```python
import os
from django.conf import settings
from django.urls.base import get_script_name
from django.utils.module_loading import module_member

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

def main():
    settings.configure()
    settings.STATIC_URL = "http://minio/static/"
    script_name = get_script_name(None, settings.STATIC_URL)
    if script_name:
        expected_url = f"{script_name}{settings.STATIC_URL}"
        actual_url = settings.STATIC_URL
        assert actual_url == expected_url, f"Expected {actual_url} but got {expected_url}"
    else:
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django configuration, sets the `STATIC_URL` setting to `"http://minio/static/"`, and then checks if the `get_script_name` function prepends the script name to the `STATIC_URL`. If it does, an `AssertionError` is raised with the expected and actual URLs.