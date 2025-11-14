import matplotlib as mpl
from io import StringIO

def main():
    try:
        rc = dict(mpl.rc_params())
        mpl.rcParams.update(rc)
        assert False, "MatplotlibDeprecationWarning was not raised"
    except MatplotlibDeprecationWarning as e:
        print_stacktrace(e)
        raise AssertionError("MatplotlibDeprecationWarning was raised")

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

if __name__ == "__main__":
    main()
