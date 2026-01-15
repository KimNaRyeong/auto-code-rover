To address your request while ensuring the script functions correctly, the following Python script `reproducer.py` is designed to reproduce the specific issue with the `random` template filter crashing on an empty list in a Django environment. To make this a self-contained example that can be run standalone without requiring a full Django project setup, we'll simulate the minimal necessary Django settings and template rendering process within the script. This allows us to focus on the issue involving the `random` filter directly.

It's important to correct the output expectations based on the logic provided in your instructions. Given the correct behavior for raising an exception when the `random` filter is used on an empty list, the script should check for this specific outcome and handle it accordingly.

```python
# reproducerer.py
import os
import django
from django.conf import settings
from django.template.base import FilterExpression, Variable, Parser
from django.template import Template, Context
from django.template.engine import Engine

def setup_django_environment():
    settings.configure(
        SECRET_KEY='this-is-just-a-reproducer',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ),
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

def reproduce_issue():
    setup_django_environment()
    template_code = '{{ list_var|random }}'
    context = {"list_var": []}
    engine = Engine.get_default()

    try:
        template = Template(template_code, engine)
        rendered = template.render(Context(context))
        assert rendered == "", "Rendered content is not empty as expected."
    except Exception as e:
        # If an IndexError is caught, that means the 'random' filter is not handling empty lists gracefully.
        if isinstance(e, IndexError):
            print("Issue detected: 'random' filter crashes with an empty list.")
            print_stacktrace(e)
            # Consider this as a successful reproduction of the issue and exit normally.
            exit(0)
        else:
            print("An unexpected error occurred while reproducing the issue.")
            print_stacktrace(e)
            exit(1)
    
    # If no exception is caught, the 'random' filter may have been silently failing or wrongly implemented.
    print("The 'random' filter did not crash as expected. The issue may have been fixed or is not reproducible.")
    exit(1)

if __name__ == "__main__":
    reproduce_issue()
```
This script is designed to:
- Setup a basic Django environment programmatically to ensure the script is self-contained.
- Define a template that uses the `random` template filter with an empty list.
- Attempt to render the template, catching and handling exceptions appropriately.
- Use the given function to print stack traces clearly when exceptions occur.
- Determine the script's exit code based on whether the issue is successfully reproduced or not.

**Please Note:** This script assumes that Django is installed in your environment. If not, you will need to install Django using pip (`pip install Django`) before running this script. Also, the behavior and output might differ based on the Django version, and this script assumes that Django's behavior regarding the `random` filter and empty lists has not drastically changed from the version described in the issue.