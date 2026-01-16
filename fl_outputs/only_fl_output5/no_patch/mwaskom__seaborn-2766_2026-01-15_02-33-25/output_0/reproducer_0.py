# reproducer.py
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

def check_warning():
    import warnings
    from setuptools._distutils.version import LooseVersion
    warnings.filterwarnings("error", category=DeprecationWarning)
    try:
        # This attempt simulates the issue where Python raises a DeprecationWarning
        # for using the LooseVersion from distutils, which is being used in a project
        # like seaborn (or any other project) indirectly through its dependencies.
        if LooseVersion("1.0.0") >= "1.0.0":
            print("Comparison succeeded without a DeprecationWarning.")
    except DeprecationWarning as e:
        print_stacktrace(e)
        raise AssertionError("DeprecationWarning was raised for distutils version classes.")

def main():
    try:
        check_warning()
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)
    else:
        print("Issue is not present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
