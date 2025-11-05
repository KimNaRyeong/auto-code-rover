Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sys
from prettytable import PrettyTable

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

def reproduce_issue():
    product = PrettyTable()
    product.field_names = ["∞", "┬───┬", "|   | 1", "|   |", "n = 1"]
    product.add_row(["∞", "┬───┬", "|   | 1", "|   |", "n = 1"])
    print(product)

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script defines a function `reproduce_issue()` that creates a `PrettyTable` instance and adds a row to it. The table is then printed using the `print()` function.

The script also defines the `print_stacktrace()` function as requested, which prints the stack trace of an exception.

In the main part of the script, we call the `reproduce_issue()` function and catch any `AssertionError` exceptions that are raised. If an exception is caught, we print the stack trace using the `print_stacktrace()` function and exit with code 1 using the `sys.exit()` function.

To reproduce the issue, simply run this script using Python: `python3 reproducer.py`.