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

def test_issue_12310():
    from sympy import Symbol, fps
    x = Symbol('x')
    try:
        p = fps(x ** 2)
        assert type(p).__name__ != 'Pow', "fps did not return a formal power series."
    except AssertionError as e:
        # If assertion fails, it means issue is present
        raise e
    except Exception as e:
        # If any other exception occurs, we print its stacktrace
        print_stacktrace(e)
    else:
        # If no exception occurs and assertion doesn't fail, issue might have been fixed
        print("The script did not raise an AssertionError, potentially indicating the issue was fixed.")
        exit(0)

if __name__ == "__main__":
    test_issue_12310()
```

This script is designed to directly assess if the `fps` function does not return a formal power series for the input `x**2` by asserting that the return type is not `Pow`. If `fps` behaves correctly, the assertion should pass (or another type of exception might be caught if the behavior is unexpected for other reasons), indicating that the issue might have been fixed. The script raises an `AssertionError` if `fps` results in a type that it should not, based on the issue statement, and prints a stack trace for any unexpected exceptions.