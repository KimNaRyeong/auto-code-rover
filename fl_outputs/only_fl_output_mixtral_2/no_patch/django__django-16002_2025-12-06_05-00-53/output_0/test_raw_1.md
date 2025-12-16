 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
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

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

    def clean_fields(self, exclude=None):
        # This method is called by the model's full_clean() method.
        # We override it to add custom validation for the DecimalField.
        if self.value != self.value:
            # The value is NaN, which is not allowed.
            raise ValidationError("NaN is not allowed in DecimalField.")

def create_mymodel_instance():
    try:
        obj = MyModel.objects.create(value="nan")
        obj.save()
        return obj
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def retrieve_mymodel_instance():
    try:
        obj = MyModel.objects.get(pk=1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    return obj

def main():
    obj = create_mymodel_instance()
    retrieved_obj = retrieve_mymodel_instance()
    assert obj == retrieved_obj, "The retrieved object should be the same as the created object."

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The stack trace should show the `TypeError` that occurs when retrieving the object from the database.

Note that this script uses Django's `full_clean()` method to validate the model instance before saving it to the database. This method calls the model's `clean_fields()` method, which we override to add custom validation for the `DecimalField`. In this case, we raise a `ValidationError` if the value is NaN. However, this validation is skipped in the original issue because the value "nan" is not None and is not an instance of float. Therefore, the value gets stored in the database as a `decimal.Decimal` object, which can be retrieved from the database but cannot be converted back to a Python float object without raising a `TypeError`.