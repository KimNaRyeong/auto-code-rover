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

try:
    import matplotlib.pyplot as plt

    # Attempt to reproduce the issue by creating and saving a zero-width figure.
    plt.subplots(1, 1, figsize=(3, 0))
    plt.savefig("test.png")

except RuntimeError as e:
    if "libpng" in str(e):
        print_stacktrace(e)
        raise AssertionError("libpng error encountered as reported.")  # This confirms the issue is present.
    else:
        print_stacktrace(e)
        raise AssertionError("Unexpected RuntimeError encountered.")  # An unexpected error occurred.
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("An unexpected exception occurred.")  # Handle any other types of exceptions.

# If the script reaches this point without exceptions, the issue has been resolved or did not occur.
print("No errors encountered. The issue appears to have been resolved.")
sys.exit(0)
