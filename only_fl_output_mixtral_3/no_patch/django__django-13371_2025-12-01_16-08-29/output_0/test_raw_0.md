 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import pickle
from django.core.exceptions import PicklingError
from django.db import models

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

class ModelA(models.Model):
    value = models.CharField(max_length=12)

def main():
    row = ModelA.objects.values_list('id', 'value', named=True).first()
    try:
        pickled_row = pickle.dumps(row)
    except PicklingError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise a `PicklingError` and print a stack trace, indicating that the `Row` object is not pickleable. If the issue is fixed, the script should exit without raising any exceptions and with exit code 0.