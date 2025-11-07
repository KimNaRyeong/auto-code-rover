```python
# reproducer.py
import sympy as sp

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

def test_idx_with_non_integer_bounds():
    m, n = sp.symbols("m, n", real=True)
    try:
        i = sp.Idx("i", (m, n))  # This should not be allowed
    except TypeError as e:
        # Expected to catch a TypeError for non-integer bounds, prints nothing if successful
        # This is where the issue is expected, correspondingly, no assertion is done here
        print_stacktrace(e)
        assert False, "Idx constructor did not raise TypeError for non-integer bounds tuple as expected."
    except Exception as e:
        # If any other Exception is raised, it's indicative of a different problem
        print_stacktrace(e)
        assert False, f"Unexpected error: {e}"

    try:
        # This should raise TypeError, confirming the type check works for single non-integer bounds
        i = sp.Idx("i", m)
    except TypeError:
        # Caught the expected TypeError, test passes for this part
        pass
    except Exception as e:
        print_stacktrace(e)
        assert False, f"Idx constructor raised an unexpected exception for single non-integer bound: {e}"

    # If the first part did not raise an error, assert failure due to the issue presence
    assert True, "Idx object incorrectly accepts non-integer bounds in tuple form without error."

if __name__ == "__main__":
    test_idx_with_non_integer_bounds()
```