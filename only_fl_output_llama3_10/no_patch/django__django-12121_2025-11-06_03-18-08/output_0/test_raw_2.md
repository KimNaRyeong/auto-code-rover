Here is the reproducer script:

```python
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

def to_url(pattern, *args, **kwargs):
    converter = pattern.converter
    value = 1 if len(args) > 0 else ''
    try:
        return converter.to_url(value)
    except ValueError:
        return ''

urlpatterns = [
    path('export/foo/<foo:obj>/', 'index', name='export'),
    path('export/bar/<bar:obj>/', 'index', name='export'),
]

if __name__ == '__main__':
    try:
        url = URLPattern(urlpatterns[0], 'export').to_url('non-matching-value')
        assert not bool(url), "Expected to_url to return an empty string"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script defines a simple Django app with two routes, and then attempts to reproduce the issue by calling `to_url` on one of the routes. If the assertion fails (i.e., `to_url` returns a non-empty string), it prints the stack trace and exits with code 1.