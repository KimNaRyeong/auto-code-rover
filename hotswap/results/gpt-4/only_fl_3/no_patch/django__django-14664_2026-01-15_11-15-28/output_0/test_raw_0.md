To create a standalone Python file named `reproducer.py` to reproduce the issue with pickling `ResolverMatch` from Django's URL resolver, especially focusing on class-based views and Django admin views, follow the code structure below. This script will attempt to serialize (pickle) the `ResolverMatch` object for both a function-based view and a class-based view and will raise an assertion error if either cannot be serialized, printing a detailed stack trace as specified.

```python
# reproducer.py
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path, resolve
from django.views import View
from pickle import dumps, loads


# Define a simple function-based view
def my_fbv(request):
    return HttpResponse('Function Based View')

# Define a simple class-based view
class MyCBV(View):
    def get(self, request):
        return HttpResponse('Class Based View')

# minimal Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    SECRET_KEY='a-secret-key',
)

urlpatterns = [
    path('fbv/', my_fbv, name='my_fbv'),
    path('cbv/', MyCBV.as_view(), name='my_cbv'),
]

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

def test_resolver_match_pickling():
    django.setup()

    # Test for function-based view
    try:
        fbv_match = resolve('/fbv/')
        dumps(fbv_match)
    except Exception as e:
        print("Failed to pickle ResolverMatch for FBV.")
        print_stacktrace(e)
        raise AssertionError("ResolverMatch for FBV is not pickleable")
    
    # Test for class-based view
    try:
        cbv_match = resolve('/cbv/')
        dumps(cbv_match)
    except Exception as e:
        print("Failed to pickle ResolverMatch for CBV.")
        print_stacktrace(e)
        raise AssertionError("ResolverMatch for CBV is not pickleable")

    print("All ResolverMatch objects successfully pickled.")

if __name__ == '__main__':
    try:
        test_resolver_match_pickling()
    except AssertionError as e:
        # Exit with code 0 to indicate an AssertionError was correctly raised for the test
        print(e)
        exit(0)
```

This script initializes a minimal Django environment, defines both a function-based and class-based view, and then attempts to pickle the `ResolverMatch` objects obtained from resolving their URLs. If an assertion error is raised due to a `PicklingError`, the stack trace will be printed using the provided `print_stacktrace` function. This script will exit with code 0 when the assertion error is correctly raised due to the issue being present.