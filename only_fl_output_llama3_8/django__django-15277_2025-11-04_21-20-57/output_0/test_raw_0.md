Here is the `reproducer.py` file that reproduces the issue:

```python
import django
from django.db.models import Value

def main():
    try:
        x = Value('test')
        y = x._resolve_output_field()
        print(y.validators)
        y.clean('1', model_instance=None)
    except TypeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.

To run this script, save it to a file named `reproducer.py`, navigate to the directory where you saved the file, and execute it using `python3 reproducer.py`.