```python
# reproducer.py
import seaborn as so
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

def run_issue_reproduction():
    try:
        # Line intended to reproduce the issue
        so.Plot(["a", "b"], [1, 2], color=[True, False]).add(so.Bar())
        # If the issue is fixed, the following line won't be reached
        print("Issue is not present, exiting with code 0.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Validating if the error matches the expected TypeError due to boolean subtraction
        assert "numpy boolean subtract" in str(e), "Unexpected error observed."
        print("Confirmed the issue with color mapping fails with boolean data.")

if __name__ == "__main__":
    run_issue_reproduction()
```

Save this script as `reproducer.py` at the root of your project and run it with `python3 reproducer.py`. This script is tailored to reproduce and confirm the issue defined by the exception related to boolean subtraction in a color mapping context with the seaborn library. When executed, it will attempt the operation known to cause the error; if the error occurs, it extracts and prints a clear stack trace as specified. If the issue is observed (i.e., the specific `TypeError` occurs), it confirms the error is as expected. If the script encounters a different error or if the operation succeeds, it will exit with code 0, indicating the issue is no longer present or was not reproduced as expected.