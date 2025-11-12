Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.template import Template, Context
from django.template.defaultfilters import random
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        django.setup()
        template = Template("{{ list_var|random }}")
        context = Context({"list_var": []})
        result = template.render(context)
        if not result:
            raise AssertionError("Expected random filter to raise an error, but it didn't.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up the Django environment using `django.setup()`, defines a template and context, attempts to render the template, and checks if the result is empty. If the `random` filter does not raise an error when given an empty list, the script raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of any exceptions that occur during the execution of the script.

Please note that this script should be executed in a directory where Django is installed.