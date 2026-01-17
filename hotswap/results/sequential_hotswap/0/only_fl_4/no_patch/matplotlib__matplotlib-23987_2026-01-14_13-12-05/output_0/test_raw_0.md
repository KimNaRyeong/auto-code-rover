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

def test_constrained_layout_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        a = np.linspace(0, 2*np.pi, 100)
        b = np.sin(a)
        c = np.cos(a)
        
        fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
        ax[0].plot(a, b)
        ax[1].plot(a, c)
        plt.subplots_adjust(wspace=0)

        # Check for UserWarning that should not be raised
        unexpected_warning_triggered = False
        for warning in w:
            if issubclass(warning.category, UserWarning) and "incompatible with subplots_adjust" in str(warning.message):
                unexpected_warning_triggered = True
                break

    if unexpected_warning_triggered:
        raise AssertionError("Constrained layout UserWarning raised even though constrained_layout is False.")

try:
    test_constrained_layout_warning()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not found, exiting with code 0.")
    exit(0)
```