import os
import sys

def test_issue():
    try:
        # Create an empty test file
        with open("test_something.py", "w") as f:
            pass

        # Run pytest with black plugin
        cmd = [sys.executable, "-m", "pytest", "--black", "test_something.py"]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        # Check if the error is present in the output
        if b"TypeError: __init__() got an unexpected keyword argument 'path'" not in output:
            print("Issue not reproduced")
            sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error reproducing the issue"

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
    test_issue()
