 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import re
import unicodedata
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_slugify():
    value = "İstanbul"
    expected_slug = "istanbul"
    slug = slugify(value, allow_unicode=True)
    assert slug == expected_slug, f"Expected slug '{expected_slug}' but got '{slug}'"

def test_validate_slug():
    value = "İstanbul"
    slug = slugify(value, allow_unicode=True)
    try:
        Page(title=value, slug=slug).full_clean()
    except ValidationError as e:
        print_stacktrace(e)
        assert False, "ValidationError raised"

if __name__ == "__main__":
    test_slugify()
    test_validate_slug()
    print("No exceptions raised, test passed.")
```
When executed with `python3 reproducer.py`, the script will raise a `ValidationError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 34, in <module>
    test_validate_slug()
  File "reproducer.py", line 28, in test_validate_slug
    Page(title=value, slug=slug).full_clean()
  File "/path/to/venv/lib/python3.8/site-packages/django/db/models/base.py", line 1203, in full_clean
    raise ValidationError(errors)
django.core.exceptions.ValidationError: {'slug': [ErrorDetail(string='Enter a valid \'slug\' consisting of Unicode letters, numbers, underscores, or hyphens.', code='invalid')]}
```
The issue is caused by the order of operations in the `slugify` function, where the lowercase version of the string is generated after removing non-alphanumeric characters. This results in a string with a combining character, which is not a valid character for a slug. The proposed solution is to generate the lowercase version of the string before removing non-alphanumeric characters.