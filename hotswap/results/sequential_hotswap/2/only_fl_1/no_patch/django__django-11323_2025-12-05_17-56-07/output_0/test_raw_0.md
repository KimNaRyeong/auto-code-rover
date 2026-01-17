 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from django import forms
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class FooForm(forms.Form):
    a_date = forms.DateField(widget=forms.SelectDateWidget)

form = FooForm()

for widget in form.fields['a_date'].widget.widgets:
    assert '<option value=""></option>' in str(widget), "First option of the select widget does not have an empty value"

```

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.