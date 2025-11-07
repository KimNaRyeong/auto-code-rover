Below is the `reproducer.py` script that sets up a minimal Django environment to reproduce the specified issue. This script will raise an `AssertionError` when encountering the described error and print a detailed stack trace. It also exits successfully (exit code 0) when the problem is fixed, meaning it won't raise an exception.

```python
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.forms import modelformset_factory

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Define a minimal Django configuration for running this script
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ],
    INSTALLED_APPS=[
        '__main__',
    ],
)

django.setup()

# Define a simple model
class MyModel(models.Model):
    a_field = models.CharField(max_length=100)

# Mimic an issue reproduction setup encapsulated in a function
def reproduce_issue():
    # Setup for reproducing the issue
    ff = modelformset_factory(MyModel, fields=['a_field'])

    try:
        # This should raise a KeyError according to the described issue
        formset = ff(
            queryset=MyModel.objects.none(),
            form_kwargs={'empty_permitted': True}
        )

        # Render the empty_form which should result in an error
        rendered = formset.empty_form.as_p()
        print("Successfully rendered; issue might be fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == '__main__':
    # A minimalist approach to execute migrations in memory for this test
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])

    try:
        reproduce_issue()
    except AssertionError as ae:
        sys.exit(1)
    else:
        sys.exit(0)
```

This script sets up a Django application in a single file, using an in-memory SQLite database, and configures minimal settings to run the test. When executed, it tries to render `formset.empty_form` with `empty_permitted` set in `form_kwargs`. If the issue described is present, it catches the exception, prints a detailed stack trace using `print_stacktrace`, and exits with code 1, indicating failure. Otherwise, it exits with code 0, indicating success or that the issue might be fixed.