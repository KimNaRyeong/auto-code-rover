Here is the reproducer script:

```python
import os
from django.conf import settings
from django.urls.resolvers import get_resolver
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
    resolver = get_resolver(None)
    try:
        url = f"/{settings.STATIC_URL}images/app-icons/favicon.ico"
        resolver.resolve(url)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django configuration, sets the `STATIC_URL` setting to `"http://minio/static/"`, and then tries to resolve a URL that starts with the `STATIC_URL`. If the issue is present, an `AssertionError` will be raised with the expected and actual URLs.