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

def test_mpl_user_warning_convert_nan():
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings

    def warning_on_show():
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
            plt.show()
            acceptable_warnings = [
                warning.category for warning in w
                if "converting a masked element to nan." in str(warning.message)
            ]
            if not acceptable_warnings:
                raise AssertionError("Expected UserWarning about converting a masked element to nan not triggered")

    try:
        warning_on_show()
    except Exception as e:
        print_stacktrace(e)
        raise

def test_mpl_stop_iteration_error():
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        fig, ax = plt.subplots(1, 1)
        ax.errorbar([0], [0], [np.nan])
        raise AssertionError("Expected StopIteration error not triggered")
    except StopIteration as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
        raise

def main():
    try:
        test_mpl_user_warning_convert_nan()
        print("Test 1 passed: No AssertionError - Issue might be fixed or not present.")
    except AssertionError as e:
        print_stacktrace(e)
    
    try:
        test_mpl_stop_iteration_error()
    except AssertionError:
        print("Test 2 passed: No StopIteration - Issue might be fixed or not present.")

if __name__ == "__main__":
    main()
```