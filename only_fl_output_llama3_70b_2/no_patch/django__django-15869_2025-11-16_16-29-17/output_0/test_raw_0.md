Here is the `reproducer.py` file:
```
from jinja2 import Template, Environment

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

env = Environment()

# Create a template with the deprecated length_is filter
template_deprecated = env.from_string("{% if value|length_is:'4' %}True{% else %}False{% endif %}")

try:
    # Render the template with a value that should pass the condition
    result_deprecated = template_deprecated.render(value="abcd")
    assert result_deprecated.strip() == "True"
    
    # Create a template with the recommended length filter and if statement
    template_recommended = env.from_string("{% if value|length == 4 %}True{% else %}False{% endif %}")
    
    # Render the template with a value that should pass the condition
    result_recommended = template_recommended.render(value="abcd")
    assert result_recommended.strip() == "True"
    
    print("Issue is fixed, exiting with code 0")
    exit(0)
except AssertionError as e:
    print_stacktrace(e)
    print("Issue is present, exiting with code 1")
    exit(1)
```
This script creates two templates: one using the deprecated `length_is` filter and another using the recommended `length` filter with an `if` statement. It then renders both templates with a value that should pass the condition and asserts that the results are as expected. If the assertions fail, it prints a stack trace of the issue and exits with code 1. If the assertions pass, it prints a success message and exits with code 0.