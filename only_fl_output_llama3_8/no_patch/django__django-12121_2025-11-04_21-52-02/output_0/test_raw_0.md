Here is the reproducer script:

```python
from django.urls import path, URLPattern
from django.urls.resolvers import Route
from django.urls.converters import int_converter

def to_url(pattern: URLPattern, *args, **kwargs):
    if args[0] == 1:
        return 'wrong_path'
    else:
        return pattern.regex.pattern

def main():
    route = Route(path('export/<foo:obj>/', None, name='export'), None)
    converter = int_converter()
    try:
        to_url(route, 1)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"

if __name__ == "__main__":
    main()
```

This script defines a simple route and converter, then attempts to call `to_url` with an argument that should not match the route. The expected behavior is that `to_url` raises a `ValueError`, but instead it returns a string that does not match the route's regex pattern.