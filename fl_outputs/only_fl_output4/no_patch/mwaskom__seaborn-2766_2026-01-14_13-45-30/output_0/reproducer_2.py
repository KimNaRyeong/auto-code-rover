import warnings
import subprocess
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

def main():
    try:
        # We'll use the subprocess module to capture warnings from stderr
        result = subprocess.run(
            [sys.executable, "-We", "-c", "import seaborn"],
            capture_output=True,
            text=True
        )

        stderr_output = result.stderr

        # Checking if the specific DeprecationWarning is present in stderr
        if "DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead." in stderr_output:
            print("The DeprecationWarning issue is present.")
        else:
            raise AssertionError("The expected DeprecationWarning is not triggered.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    # Exiting with code 0 to signify future version where issue may be resolved.
    print("Issue fixed or not present.")
    sys.exit(0)

if __name__ == "__main__":
    main()
