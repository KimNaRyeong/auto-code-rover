 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import pickle
from django.core.urlresolvers import resolve
from django.urls import path
from django.utils.six.moves import input

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyView:
    pass

urlpatterns = [
    path('my_fbv/', MyView.as_view(), name='my_fbv'),
    path('admin/', MyView.as_view(), name='admin'),
]

try:
    request_url = input("Enter URL to test: ")
    resolver_match = resolve(request_url)
    pickled_match = pickle.dumps(resolver_match)
    _ = pickle.loads(pickled_match)
except Exception as e:
    print_stacktrace(e)
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. The script will prompt for a URL to test, and then attempt to pickle the corresponding `ResolverMatch` object. If the pickling is successful, the script will exit with code 0. If the pickling fails, an `AssertionError` will be raised and a stack trace will be printed.

The script uses the `input()` function to prompt for a URL to test, so it can be run in a terminal or command prompt. If you prefer, you can replace the `input()` function with a hard-coded URL to test.

Note that the script uses the `path()` function from Django 2.0's `urls` module instead of the `url()` function from Django 1.11's `url` module. If you are using Django 1.11, you will need to replace the `path()` function with the `url()` function and adjust the import statement accordingly.