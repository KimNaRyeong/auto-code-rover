# reproducer.py
import os
import sys
from unittest import mock

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

def matplotlib_import_test():
    try:
        with mock.patch("locale.getpreferredencoding", return_value="UTF-32-BE"):
            # Importing matplotlib inside the function to ensure it gets the patched encoding
            import matplotlib.pyplot as plt
            plt.figure()
        assert False, "The issue is not present or the test did not reproduce it correctly."
    except UnicodeDecodeError as e:
        print_stacktrace(e)
        assert True, "The issue is present"
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred"

if __name__ == "__main__":
    matplotlib_import_test()
