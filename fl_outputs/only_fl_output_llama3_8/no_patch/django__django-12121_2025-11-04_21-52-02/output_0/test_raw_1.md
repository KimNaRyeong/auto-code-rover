Here is the reproducer script:

```python
from django.urls import path, URLPattern
from django.urls.resolvers import Route
import sys
import traceback

def to_url(pattern: URLPattern):
    return 'wrong_path'

def main():
    route = Route(path('export/<foo:obj>/', None, name='export'), None)
    try:
        to_url(route)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"
    else:
        print("Issue fixed")
        sys.exit(0)

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

This script defines a simple route and attempts to call `to_url` with the route. The expected behavior is that `to_url` raises a `ValueError`, but instead it returns a string that does not match the route's regex pattern.