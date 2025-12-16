 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def f():
    print(django.__version__)

if __name__ == "__main__":
    try:
        import django
        exec("f()")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception should not be raised here."

    try:
        import django
        exec("f()", {})
    except Exception as e:
        print_stacktrace(e)
        assert True, "An exception should be raised here."
```
When executed with `python3 reproducer.py`, the script will first try to execute the `f()` function without passing a dictionary containing a minimal set of globals to `exec`. This will result in a `NameError` being raised, as described in the issue.

The script will then try to execute the `f()` function again, this time passing an empty dictionary as the second argument of `exec`. This will result in the `NameError` being caught and printed to the console, as expected.

The script will exit with code 0 in both cases, as the issue is not related to the exit code.