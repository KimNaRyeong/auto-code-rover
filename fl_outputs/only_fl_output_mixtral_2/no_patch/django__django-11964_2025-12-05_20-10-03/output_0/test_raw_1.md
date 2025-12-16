 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from enum import Enum
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyChoice(models.TextChoices):
    FIRST_CHOICE = "first", "The first choice, it is"
    SECOND_CHOICE = "second", "The second choice, it is"

class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=MyChoice.choices)

def main():
    my_object = MyObject(my_str_value=MyChoice.FIRST_CHOICE)
    my_object.save()

    # This assertion fails because my_object.my_str_value is of type MyChoice,
    # not str.
    assert str(my_object.my_str_value) == "first"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, create a new Django project and add the above code to a file named `reproducer.py` in the root directory of the project. Then run the script with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace showing the line where the assertion fails.

To fix the issue, you can change the type of the `my_str_value` field to `str` and use the `choices` attribute of the `MyChoice` enum as follows:
```python
class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in MyChoice])
```
This will ensure that the value of `my_str_value` is always a string.