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
    import warnings
    from packaging import version

    # Attempt to catch the DeprecationWarning as an error to verify if it exists
    warnings.filterwarnings("error", category=DeprecationWarning)
    try:
        # This import should trigger the DeprecationWarning
        # if the issue is present due to the seaborn or setuptools dependency.
        import seaborn
        # Replace the version check below with the fixed version once known.
        # if version.parse(seaborn.__version__) < version.parse("FIXED_VERSION"):
        #     raise AssertionError("DeprecationWarning is triggered by seaborn")
    except DeprecationWarning as e:
        print_stacktrace(e)
        raise AssertionError("DeprecationWarning is triggered by seaborn")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError(f"Unexpected exception: {e}")

    print("No DeprecationWarning triggered. The issue seems fixed.")

if __name__ == "__main__":
    main()
