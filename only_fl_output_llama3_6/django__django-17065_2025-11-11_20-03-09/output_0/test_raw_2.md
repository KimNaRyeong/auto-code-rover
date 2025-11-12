Here is the reproducer script in a code block:

```python
import django
from django.forms import Form, CharField
from django.test import SimpleTestCase

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

def main():
    class TestForm(Form):
        data = CharField(help_text="Some help text")

    form = TestForm({"data": "some value"})
    self = assertHTMLEqual
    try:
        form["data"].as_widget(attrs={"aria-describedby": "custom_help_text_id"})
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
```

This script defines a test case that attempts to reproduce the issue. It creates a `TestForm` with a single field and then calls `as_widget()` on that field, passing in an `attrs` dictionary with an `aria-describedby` attribute. The test expects this call to raise an `AssertionError`.