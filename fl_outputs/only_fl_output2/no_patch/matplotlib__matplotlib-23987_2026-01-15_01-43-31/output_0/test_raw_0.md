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


def test_constrained_layout_warning():
    import matplotlib.pyplot as plt
    import numpy as np
    import warnings

    a = np.linspace(0, 2 * np.pi, 100)
    b = np.sin(a)
    c = np.cos(a)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
        ax[0].plot(a, b)
        ax[1].plot(a, c)
        plt.subplots_adjust(wspace=0)

        # Check if any UserWarning was raised that matches our case
        constrained_layout_warning_fired = any(
            "constrained_layout=False" in str(warning.message) and
            "incompatible with subplots_adjust" in str(warning.message)
            for warning in w
        )

    # Raise an AssertionError if the specific warning is found
    assert not constrained_layout_warning_fired, "Constrained layout warning fired even when set to False."


if __name__ == "__main__":
    try:
        test_constrained_layout_warning()
        print("Test Passed: No issues found.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)  # Ensures the exit code is non-zero when assertion fails
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        raise SystemExit(0)
```