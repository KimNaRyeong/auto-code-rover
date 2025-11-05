Here is the reproducer script in a code block:

```python
import django
from django.db.models import Value

def main():
    try:
        x = Value('test')
        y = x._resolve_output_field()
        print(f"Before fix: {y.validators}")
        y.clean('1', model_instance=None)
    except TypeError as e:
        print_stacktrace(e)

    if 'test' in str(y.validators):
        raise AssertionError("Issue not reproduced")

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

if __name__ == "__main__":
    django.setup()  # Initialize Django
    main()

    if 'test' not in str(y.validators):
        exit(0)