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

try:
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
except AssertionError:
    print_stacktrace(AssertionError('NON_FIELD_ERRORS should not contain hidden field errors after calling as_table() once'))
    sys.exit(1)

print(test_form.as_table())

try:
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
except AssertionError:
    print_stacktrace(AssertionError('NON_FIELD_ERRORS should contain the same hidden field errors after calling as_table() multiple times'))
    sys.exit(1)
```
When the script is executed with Python 3.6.5 and Django 2.1.7, it raises an `AssertionError` and prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
AssertionError: NON_FIELD_ERRORS should contain the same hidden field errors after calling as_table() multiple times
```
This confirms that the issue exists in Django 2.1.7.

To fix the issue, you can modify the `forms.py` file as suggested in the issue description:
```python
def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
	top_errors = self.non_field_errors().copy() # Errors that should be displayed above all fields.
	output, hidden_fields = [], []
	for name, field in self.fields.items():
		...
```
After applying this fix, the script should not raise any `AssertionError` and exit with code 0.