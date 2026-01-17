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
    import matplotlib as mpl
    import warnings

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        rc = dict(mpl.rc_params())
        mpl.rcParams.update(rc)
        # Check if any MatplotlibDeprecationWarning has been raised
        matplotlib_deprecation_warnings = [
            warning for warning in w if issubclass(warning.category, mpl.MatplotlibDeprecationWarning)
        ]
        if matplotlib_deprecation_warnings:
            raise AssertionError(f"Found {len(matplotlib_deprecation_warnings)} MatplotlibDeprecationWarning(s)")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("No issue found. Exiting with code 0.")
        raise SystemExit(0)
```