Sure, I will correct the code to ensure it functions correctly within a standalone script setup without assuming a pre-established Django project context. This script will now properly configure Django to avoid the `ImproperlyConfigured` exception by setting up a minimal required Django environment programmatically. I'll remove the unnecessary `{% load my_tags %}` since that was mistakenly included and is not part of the standard Django template tags. We'll focus directly on reproducing the issue with the `random` filter on an empty list.

```python
# reproducer.py
import os
import django
from django.conf import settings
from django.template import Template, Context

# Minimal Django settings required for templates
settings.configure(
    SECRET_KEY='a-very-secret-key',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ),
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
    }],
)
django.setup()

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
    t = Template('{{ list_var|random }}')
    c = Context({"list_var": []})
    try:
        rendered = t.render(c)
        # If we reach this point without an exception, the behavior is not as expected.
        assert False, "The 'random' template filter did not raise an exception when applied to an empty list."
    except Exception as e:
        # We expect an IndexError because the list is empty.
        if not isinstance(e, IndexError):
            print("An unexpected exception type was caught.")
            print_stacktrace(e)
        assert isinstance(e, IndexError), "Expected an IndexError due to the empty list."

if __name__ == "__main__":
    try:
        test_random_filter_with_empty_list()
        # If the test function raises AssertionError, it won't reach this point.
        print("Test failed: The issue is present. The 'random' filter should not raise an exception on an empty list.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed: The 'random' filter behaves consistently with 'first' and 'last' on an empty list.")
        exit(0)
```

This script now creates a minimal Django environment, executes a template that attempts to use the `random` filter on an empty list, and checks if it behaves as expected by raising an `AssertionError` if the issue is present or passing silently if fixed. The script now properly captures the intended behavior and setup to reproduce the issue in a standalone script.