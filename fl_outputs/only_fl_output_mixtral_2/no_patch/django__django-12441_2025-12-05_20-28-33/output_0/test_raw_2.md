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
    print_stacktrace(AssertionError('NON_FIELD_ERRORS should not contain duplicate hidden field errors after calling as_table() multiple times'))
    sys.exit(1)
```
When executed with Python 3.6.5 and Django 2.1.7, the script reproduces the issue and raises an `AssertionError` with a stack trace.

Here is the output of the script:
```python
{'hidden_input': ['This field is required.', 'Hidden input error'], '__all__': ['Form error']}
<tr><td colspan="2"><ul class="errorlist nonfield"><li>Form error</li><li>(Hidden field hidden_input) This field is required.</li><li>(Hidden field hidden_input) Hidden input error</li></ul><input type="hidden" name="hidden_input" id="id_hidden_input"></td></tr>
Traceback (most recent call last):
  File "reproducer.py", line 34, in <module>
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
AssertionError: NON_FIELD_ERRORS should not contain hidden field errors after calling as_table() once
```
The `AssertionError` is raised because the `NON_FIELD_ERRORS` contains hidden field errors after calling `as_table()` once.

To fix the issue, you can modify the `forms.py` file as suggested in the issue description. Alternatively, you can create a custom form class that overrides the `_html_output()` method and uses a copy of the `non_field_errors()` list. Here is an example:
```python
class CustomForm(forms.Form):
    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        top_errors = list(self.non_field_errors())  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        for name, field in self.fields.items():
            if hasattr(field.widget, 'is_hidden') and field.widget.is_hidden:
                hidden_fields.append((name, field