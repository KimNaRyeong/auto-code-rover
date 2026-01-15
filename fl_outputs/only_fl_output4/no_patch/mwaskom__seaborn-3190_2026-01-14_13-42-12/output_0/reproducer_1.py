# reproducer.py
import sys

try:
    import seaborn as so
except ImportError as e:
    print("Required module 'seaborn' is not installed, attempting to install...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])
    # Retry the import after installation
    import seaborn as so

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
        # Checking for the specific error to confirm the issue
        assert "numpy boolean subtract" in str(e), "Unexpected error observed."
        print("Confirmed the issue with color mapping fails with boolean data.")

if __name__ == "__main__":
    run_issue_reproduction()
