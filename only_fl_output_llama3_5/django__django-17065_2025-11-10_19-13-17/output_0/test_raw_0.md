Here is the reproducer script in a code block:

```python
import django
from django.test import SimpleTestCase
from django.forms import Form, CharField

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

class Reproducer(SimpleTestCase):
    def test_as_widget_ignores_aria_describedby(self):
        class TestForm(Form):
            data = CharField(help_text="Some help text")
        form = TestForm({"data": "some value"})
        self.form = form
        with self.assertRaises(AssertionError):
            self.assertHTMLEqual(
                self.form["data"].as_widget(attrs={"aria-describedby": "custom_help_text_id"}),
                """
                <input type="text" name="data" value="some value"
                aria-describedby="" required id="id_data">
                """,
            )

if __name__ == "__main__":
    try:
        Reproducer().run()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script creates a test case that reproduces the issue. It defines a custom form with a single field and then uses `BoundField.as_widget()` to render the field's widget, passing in an `attrs` dictionary with an `aria-describedby` attribute. The script then asserts that the rendered HTML does not include the expected `aria-describedby` attribute value.

If the issue is present (i.e., the `aria-describedby` attribute is ignored), the script will raise an `AssertionError`, print a stack trace, and exit with code 1. If the issue is fixed, the script will simply exit with code 0.