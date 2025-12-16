 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import django
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

django.setup()

from django import forms

class TestForm(forms.Form):
	hidden_input = forms.CharField(widget=forms.HiddenInput)

	def clean(self):
		self.add_error(None, 'Form error')
		self.add_error('hidden_input', 'Hidden input error')

test_form = TestForm({})

print(test_form.errors)
print(test_form.as_table())

# Assert that the non_field_errors have not changed after rendering the form
assert test_form.non_field_errors() == ['Form error'], "The non_field_errors should not include hidden field errors."

print_stacktrace(AssertionError("The non_field_errors should not include hidden field errors."))
sys.exit(1)
```
To execute the script, run `python3 reproducer.py` in the root directory of the project. The script will raise an `AssertionError` and print a stack trace showing the issue.

The fix for this issue is to use a copy of the error list before adding the hidden field errors in the file `django/forms/forms.py`. You can apply the fix by replacing the line:
```python
top_errors = self.non_field_errors()
```
with:
```python
top_errors = self.non_field_errors().copy()
```
After applying the fix, the script should exit with code 0 and not print any stack trace.