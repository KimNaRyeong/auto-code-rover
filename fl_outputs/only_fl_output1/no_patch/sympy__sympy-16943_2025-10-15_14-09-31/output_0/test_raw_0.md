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

def main():
    from sympy import Symbol, fps, FormalPowerSeries
    x = Symbol('x')
    try:
        p = fps(x ** 2)
        # Verifying that the result is an instance of FormalPowerSeries
        assert isinstance(p, FormalPowerSeries), "Expected instance of FormalPowerSeries, got {}".format(type(p))
        print("Issue #12310 is fixed.")
    except AssertionError as ex:
        print_stacktrace(ex)
        raise ex
    except Exception as e:
        print("An unexpected error occurred:", e)
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by calling the `fps` function with \( x^2 \) as its argument, expecting the return value to be an instance of `FormalPowerSeries`, as would be indicated if the issue were fixed. If the function returns a `Pow` object (or anything else that is not a `FormalPowerSeries`), the script will raise an `AssertionError` and print a stack trace specific to the error context, indicating that the issue is still present. If the issue is fixed, it will simply print a message indicating so and exit with code 0.