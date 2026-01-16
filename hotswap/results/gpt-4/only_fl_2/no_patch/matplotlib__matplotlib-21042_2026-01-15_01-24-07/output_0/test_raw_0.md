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
        warnings.simplefilter("always")  # Trigger all warnings
        rc = dict(mpl.rc_params())
        mpl.rcParams.update(rc)

        # Check if any deprecation warnings for rcParams were caught
        deprecation_warnings = [x for x in w if x.category == mpl.MatplotlibDeprecationWarning and 'rcparam' in str(x.message)]
        try:
            assert not deprecation_warnings, "DeprecationWarnings for rcParams were raised"
        except AssertionError as e:
            print_stacktrace(e)
            raise e

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        # If an assertion error is caught, it means the issue is present. Exit with non-zero code.
        import sys
        sys.exit(1)
    else:
        # If no errors, exit cleanly.
        sys.exit(0)
```