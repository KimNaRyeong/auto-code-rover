```python
import matplotlib.pyplot as plt
import numpy as np
import warnings

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

def test_warning():
    """
    This test checks if a UserWarning is raised when using `plt.subplots_adjust` with `constrained_layout=False`.
    The expected behavior is that it should not raise a Warning.
    """
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")  # Trigger all warnings to be caught
            # Code that should generate the warning if the issue is present
            a = np.linspace(0, 2 * np.pi, 100)
            b = np.sin(a)
            c = np.cos(a)
            fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
            ax[0].plot(a, b)
            ax[1].plot(a, c)
            plt.subplots_adjust(wspace=0)  # This is where the warning would be triggered

            if w:  # If the list is not empty, warnings were raised
                for warning in w:  # Checking for UserWarning
                    if issubclass(warning.category, UserWarning):
                        if "incompatible with subplots_adjust" in str(warning.message):
                            raise AssertionError("UserWarning for incompatible layout detected with constrained_layout=False")
        
        print("No warning raised. Test passed.")

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_warning()
```