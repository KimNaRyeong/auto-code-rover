```python
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

def check_seaborn_warning():
    result = subprocess.run([
            sys.executable, '-We', '-c',
            'import seaborn'
        ], 
        capture_output=True, text=True
    )

    # Check if the DeprecationWarning appears in stderr
    if "DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead." in result.stderr:
        raise AssertionError("DeprecationWarning for distutils version classes detected.")

if __name__ == "__main__":
    try:
        check_seaborn_warning()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate the issue is present
    sys.exit(0)  # Exit with code 0 to indicate the issue is fixed
```