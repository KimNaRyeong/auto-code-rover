Sure, here is a standalone Python script `reproducer.py` that reproduces the reported issue. It's designed to exit with code 0 if the issue is fixed and to print a detailed stack trace if the exception is raised due to the problem.

```python
from sympy import symbols, DiracDelta, pprint
from sympy.core.compatibility import as_int
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    x = symbols('x')
    try:
        pprint(x*DiracDelta(x, 1))
    except TypeError as e:
        print_stacktrace(e)
        # Checking if the TypeError is specifically about unorderable types
        assert "unorderable types: NoneType() > int()" in str(e), "Issue not reproduced correctly."
        print("Issue reproduced successfully.")
        return
    print("No issue detected, perhaps the problem has been fixed.")

if __name__ == "__main__":
    test_issue()
```

To use this script, simply save it as `reproducer.py` in the root of the SymPy project directory (assuming SymPy is installed and accessible in your Python environment), and then run `python3 reproducer.py` from your terminal. If the issue is present, the script will print the detailed stack trace as mentioned and assert successfully, indicating the problem. If no issue is found (i.e., if SymPy's developers have fixed it), the script will exit normally with the message "No issue detected, perhaps the problem has been fixed."