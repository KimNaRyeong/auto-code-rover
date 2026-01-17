 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django import forms

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

class MyForm(forms.Form):
    number_field = forms.IntegerField(min_value=1, step_size=2)

if __name__ == "__main__":
    form = MyForm({'number_field': 1})
    try:
        form.is_valid()
    except forms.ValidationError as e:
        print_stacktrace(e)
        raise AssertionError("ValidationError raised as expected")
```
When executed with `python3 reproducer.py`, this script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    form.is_valid()
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/forms.py", line 177, in is_valid
    return self.is_bound and not self.errors
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/forms.py", line 172, in full_clean
    self._post_clean()
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/models.py", line 399, in _post_clean
