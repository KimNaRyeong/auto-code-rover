Here is the reproducer script in a code block:

```python
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

import django
from django.forms import Form, CharField

def reproduce_issue():
    class TestForm(Form):
        data = CharField(help_text="Some help text")
    form = TestForm({"data": "some value"})

    try:
        self.assertHTMLEqual(
            form["data"].as_widget(attrs={"aria-describedby": "custom_help_text_id"}),
            """
            <input type="text" name="data" value="some value"
            aria-describedby="" required id="id_data">
            """,
        )
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script should be executed by `python3 reproducer.py`. It will raise an `AssertionError` when the issue is present and print a stack trace of the issue.