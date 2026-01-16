```python
# reproducer.py

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
    import numpy as np
    from sklearn import set_config
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.linear_model import SGDClassifier

    try:
        set_config(transform_output="pandas")
        model = CalibratedClassifierCV(SGDClassifier(), method='isotonic')
        model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
        model.predict(np.arange(90).reshape(30, -1))
        # If no exception has occurred, we assume the issue has been fixed
        print("The issue appears to be fixed.")
    except ValueError as e:
        print_stacktrace(e)
        # Ensure that this script only captures the specific issue we're interested in.
        assert "could not broadcast input array from shape" in str(e), "An unrelated ValueError occurred."
        exit(1)  # Exit with code non-zero to indicate failure.
    except Exception as e:
        # Catch-all for other exceptions, including potential new ones introduced by a fix.
        print("An unexpected exception occurred:", str(e))
        print_stacktrace(e)
        exit(1)  # Exit with code non-zero to indicate an unexpected failure.

if __name__ == "__main__":
    main()
```

This script will attempt to reproduce the described issue with `CalibratedClassifierCV` and `set_config(transform_output="pandas")` incompatibility. If the specific `ValueError` is raised, it will print the stack trace as required and exit with code 1. If the issue is fixed, the script will simply print a message saying the issue appears to be fixed and exit with code 0. The use of an `assert` statement ensures that only the specific error indicating the issue is present will cause the script to confirm the issue; any other `ValueError` or exception will lead to an exit with code 1 but for different reasons, indicating either a different error has occurred or that something unexpected has happened.