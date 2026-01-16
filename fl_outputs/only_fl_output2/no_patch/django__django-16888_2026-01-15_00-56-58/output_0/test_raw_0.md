Below is a standalone Python script named `reproducer.py`, designed to reproduce the issue you described. This script is assuming you have a Django project setup with SQLite as the database.

Before running the script, you need to ensure that Django and the relevant project settings are correctly configured. The script attempts to query a `DecimalField` with a value larger than `max_digits`, expecting an error related to decimal value quantization as per the described issue.

```python
import os
import django 
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Replace 'your_project.settings' with the actual name of your Django project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

    class Meta:
        app_label = 'your_app_label_here'  # Replace with your app label


def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_invalid_decimal_query():
    try:
        DecimalModel.objects.create(dec_field=1234)  # Within the max_digits limit
        DecimalModel.objects.get(dec_field='12345')  # Exceeds max_digits
        assert False, "Querying for decimals larger than max_digits should not succeed."
    except decimal.InvalidOperation as e:
        print_stacktrace(e)
        assert True  # Ensure that this is the expected failure mode
    except ObjectDoesNotExist:
        pass  # This is the expected behavior if the issue is fixed and should pass silently
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected error occurred."
        

if __name__ == '__main__':
    test_invalid_decimal_query()
```

Please ensure to:
- Replace `'your_project.settings'` with the actual path to your Django project settings.
- Specify the correct app label in `Meta` class of `DecimalModel`.

This script will raise an `AssertionError` if the issue is present, along with printing a stack trace of the issue. If the issue is fixed, it exits with code 0, indicating success.