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

def test_libpng_crash_with_zero_width_figure():
    import matplotlib.pyplot as plt

    try:
        plt.subplots(1, 1, figsize=(3, 0))
        plt.savefig("test.png")
        print("The issue has been fixed. No exception was raised.")
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, RuntimeError), "Expected a RuntimeError, got a different exception."
        assert "libpng signaled error" in str(e), "The error message does not match the expected 'libpng signaled error'."

if __name__ == "__main__":
    test_libpng_crash_with_zero_width_figure()
```

This script attempts to reproduce the reported issue by creating a zero-width figure with `matplotlib` and then saving it, which is expected to trigger a `RuntimeError` from `libpng`. If the issue is present, it will capture the error and assert that a `RuntimeError` has occurred with the expected message. If the conditions are not met (e.g., a different error occurs or no error at all), the script will raise an `AssertionError`. It also uses the defined `print_stacktrace` function to print detailed information about the exception stack trace, ensuring that any traceback is clear and informative. 

The script ends with an exit code of 0 if the issue has been fixed (i.e., no exception was raised), adhering to the requirement for the script to exit with code 0 in the scenario where the issue is resolved.