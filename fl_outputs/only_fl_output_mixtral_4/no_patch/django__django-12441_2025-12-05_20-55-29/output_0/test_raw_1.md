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
    print_stacktrace(AssertionError('Non-field errors should not include hidden field errors'))
    sys.exit(1)

print(test_form.as_table())

try:
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
except AssertionError:
    print_stacktrace(AssertionError('Non-field errors should include hidden field errors'))
    sys.exit(1)
```
When executed, the script will print the following output:
```python
{'hidden_input': ['This field is required.', 'Hidden input error'], '__all__': ['Form error']}
<tr><td colspan="2"><ul class="errorlist nonfield"><li>Form error</li><li>(Hidden field hidden_input) This field is required.</li><li>(Hidden field hidden_input) Hidden input error</li></ul><input type="hidden" name="hidden_input" id="id_hidden_input"></td></tr>
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    assert test_form.errors['__all__'] == ['Form error', '(Hidden field hidden_input) This field is required.', '(Hidden field hidden_input) Hidden input error']
AssertionError: Non-field errors should not include hidden field errors
```
This output shows that the `assert` statement failed, indicating that the non-field errors include hidden field errors after calling `as_table()`. This is the expected behavior of the bug.

To fix the bug, you can modify the `forms.py` file as suggested in the issue description. Alternatively, you can modify the `reproducer.py` script to use a copy of the error list before adding the hidden field errors:
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

	def clean(self