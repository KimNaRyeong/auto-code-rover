```python
# reproducer.py
import matplotlib.pyplot as plt
import numpy as np
import warnings
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    a = np.linspace(0, 2 * np.pi, 100)
    b = np.sin(a)
    c = np.cos(a)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Trigger plot creation and potential warning
        fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
        ax[0].plot(a, b)
        ax[1].plot(a, c)
        plt.subplots_adjust(wspace=0)

        # Check for warnings
        unexpected_warnings = [warn for warn in w if "constrained_layout" in str(warn.message)]
        try:
            assert not unexpected_warnings, "Expected no constrained_layout UserWarning"
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)  # Exit with error if the issue is present

if __name__ == "__main__":
    main()
    print("Issue not present.")  # This should be printed if the bug is fixed.
    sys.exit(0)  # Exit code 0 when the issue is fixed.
```