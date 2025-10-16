Certainly, let's create a standalone `reproducer.py` script that follows the given structure and guidance. The script will initialize a minimal Django application, define the required models, and run test cases to reproduce the issue. It is designed to demonstrate the issue as described, where the `Exists` annotation with an empty `QuerySet` returns `None` instead of a boolean value. 

```python
"""
reproducer.py
"""
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Exists

# Minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
)

django.setup()

# Defining our test models
class A(models.Model):
    pass

class B(models.Model):
    pass

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

def run_tests():
    # Creating instances of our models (optional as they are not used directly in queries)
    A.objects.create()
    B.objects.create()

    # Conduct tests to check if Exists returns a non-boolean value
    result_with_empty_qs = A.objects.annotate(empty_qs=Exists(B.objects.none())).first().empty_qs

    # We add explicit assertions to capture two cases:
    # 1. The result should not be None
    # 2. The result should be a boolean value
    try:
        assert result_with_empty_qs is not None, "Exists with an empty QuerySet returned None."
        assert isinstance(result_with_empty_qs, bool), f"Expected a boolean value but got {type(result_with_empty_qs)}."
        print("Test passed: Exists with an empty QuerySet returned a boolean value.")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    run_tests()
```

This script initializes a Django environment with two models, `A` and `B`, directly in the script to keep the reproduction case as self-contained and straightforward as possible. It then tests whether annotating a queryset of `A` with an `Exists` query on an empty queryset of `B` returns an appropriate boolean value, or leads to an error indicative of the documented issue.

Make sure you have Django installed in your environment when you run this script. You can install Django by running `pip install django` in your terminal or command prompt. After ensuring Django is installed, you can execute the script with `python3 reproducer.py`.

Note: This script is configured to use SQLite. If the original issue was observed with another database (like PostgreSQL, as mentioned), adjustments to the `DATABASES` configuration within the script will be necessary to accurately reproduce the issue in those environments.