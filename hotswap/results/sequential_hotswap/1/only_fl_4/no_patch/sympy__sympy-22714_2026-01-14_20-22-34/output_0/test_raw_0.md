Here is a standalone Python script named `reproducer.py` that you can use to reproduce the issue described. When the issue is present, it raises an `AssertionError` and prints the stack trace of the issue. It exits with code 0 when the issue is resolved. Make sure to put this script in the root directory of your project and run it with `python3 reproducer.py`.

```python
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

def reproducer():
    import sympy as sp
    try:
        with sp.evaluate(False):
            sp.S('Point2D(Integer(1),Integer(2))')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    try:
        sp.S('Point2D(Integer(1),Integer(2))')
        sp.S('Point2D(Integer(1),Integer(2))', evaluate=False)
        return 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpectedly failed outside the context manager.")

if __name__ == "__main__":
    reproducer()
```

This script tries to execute the problematic code block inside a `try-except` block to catch the exception and print a detailed stack trace using the `print_stacktrace` function provided. It then attempts the operations that are expected to succeed outside the `with sp.evaluate(False)` context manager, ensuring that if any unexpected failure occurs there, it's also caught and reported. 

Running this script should help you pinpoint the problem by showing exactly where in your code and the Sympy library the error occurs, and it acts as a direct indicator when the underlying issue is resolved, since it only raises an `AssertionError` if the problem is currently present.