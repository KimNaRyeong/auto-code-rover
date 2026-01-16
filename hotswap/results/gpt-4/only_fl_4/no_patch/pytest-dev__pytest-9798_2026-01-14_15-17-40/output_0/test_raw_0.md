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

def test_approx_without_numpy():
    # We attempt to reproduce the ModuleNotFoundError for Numpy
    # when pytest.approx fails as described.
    import pytest
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print("An unexpected exception occurred:", str(e))
        raise e

if __name__ == '__main__':
    try:
        test_approx_without_numpy()
    except ModuleNotFoundError as e:
        if e.name == 'numpy':
            print("Issue is present: ModuleNotFoundError for Numpy when pytest.approx fails.")
        else:
            print("Unexpected ModuleNotFoundError:", e.name)
    except AssertionError:
        print("The assertion failed as expected, but no ModuleNotFoundError for Numpy was raised. The issue is fixed.")
        exit(0)
    except Exception as general_exception:
        print("An unexpected error occurred:", str(general_exception))
        raise general_exception
```