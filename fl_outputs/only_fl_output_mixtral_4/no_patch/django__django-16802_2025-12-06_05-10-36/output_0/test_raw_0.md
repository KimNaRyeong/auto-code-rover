 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from django.template import Template, Context
from django.template.defaultfilters import random
import django

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


def main():
    django.setup()

    t = Template("""
    {% load static %}
    <html>
    <body>
        <ul>
            {% for item in list_var %}
                <li>{{ item }}</li>
            {% empty %}
                <li>Empty list</li>
            {% endfor %}
        </ul>
        <ul>
            <li>First: {{ list_var|first }}</li>
            <li>Last: {{ list_var|last }}</li>
            <li>Random: {{ list_var|random }}</li>
        </ul>
    </body>
    </html>
    """)

    c = Context({"list_var": []})

    try:
        output = t.render(c)
        assert False, "Expected an exception to be raised"
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the `IndexError` raised by the `random` filter when applied to an empty list. This reproduces the issue described in the given report.

Note that the `print_stacktrace` function is used to print the stack trace in a format that shows the line numbers of the statements clearly.