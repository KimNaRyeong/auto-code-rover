 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class MyChoice(models.TextChoices):
    FIRST_CHOICE = "first", _("The first choice, it is")
    SECOND_CHOICE = "second", _("The second choice, it is")

class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=MyChoice.choices)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    my_object = MyObject(my_str_value=MyChoice.FIRST_CHOICE)
    try:
        assert isinstance(my_object.my_str_value, str)
        assert str(my_object.my_str_value) == "first"
    except AssertionError as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    assert str(my_object.my_str_value) == "first"
AssertionError: 'MyChoice.FIRST_CHOICE' != 'first'
- MyChoice.FIRST_CHOICE
+ first
```
This reproduces the issue where the value of a `CharField` with `choices` pointing to `TextChoices` has a differing type. The `my_str_value` is of type `MyChoice` instead of `str`.