```python
# reproducer.py
from django.template import Template, Context
from django.conf import settings
import os

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
settings.configure()

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

def test_random_filter_with_empty_list():
    t = Template('{% load my_tags %}{{ list_var|random }}')
    c = Context({"list_var": []})
    try:
        rendered = t.render(c)
    except Exception as e:
        # If an exception is raised, let's print the stack trace and fail the test
        print_stacktrace(e)
        raise AssertionError("The 'random' template filter should not raise exception when applied to an empty list.") from None      
    else:
        # If no exception is raised, that's an unexpected behavior as well
        assert rendered == '', "Expected empty string for empty list with 'random' filter."
        print("Test Passed: No AssertionError raised.")

if __name__ == "__main__":
    test_random_filter_with_empty_list()
```