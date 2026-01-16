```python
# reproducer.py

import os
import sys
from django.conf import settings
from django.template import Template, Context


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


def setup_django_environment():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='asecrettoeverybody',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
            },
        ],
    )
    try:
        import django
        django.setup()
    except AttributeError as e:
        print_stacktrace(e)
        sys.exit(1)


def reproduce_issue():
    faulty_template_string = "{{ list_var|random }}"
    template = Template(faulty_template_string)
    context = Context({"list_var": []})
    
    try:
        output = template.render(context)
        # Since the issue is that an empty list causes a crash,
        # we expect not to reach this point without an error.
        assert output != "", "Expected an exception to be raised for an empty list with the 'random' filter."
    except Exception as e:
        print_stacktrace(e)
        # If an IndexError is raised, it confirms the reported issue.
        if isinstance(e, IndexError):
            print("Issue confirmed: 'random' filter causes IndexError on an empty list.")
            sys.exit(0)
        else:
            # If any other exception is raised, it's a different issue.
            sys.exit(1)


if __name__ == "__main__":
    setup_django_environment()
    reproduce_issue()
```