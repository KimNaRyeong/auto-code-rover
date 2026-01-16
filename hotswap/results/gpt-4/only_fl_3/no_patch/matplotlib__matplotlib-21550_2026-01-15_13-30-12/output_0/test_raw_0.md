```python
import traceback
import sys
import matplotlib


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def check_matplotlib_version():
    # Extract major, minor and patch version from matplotlib
    version_parts = matplotlib.__version__.split(".")
    major = int(version_parts[0])
    minor = int(version_parts[1])
    if 'dev' in version_parts[2]:  # Handle development versions
        patch = int(version_parts[2].split('dev')[0])
    else:
        patch = int(version_parts[2])
    return major, minor, patch


def main():
    try:
        major, minor, patch = check_matplotlib_version()
        # Checking for the version in question
        if (major, minor, patch) == (3, 5, 0):
            raise AssertionError("Matplotlib version 3.5.0 is known to have this issue.")
        else:
            print(f"Matplotlib version is {major}.{minor}.{patch}, which is not affected by this issue.")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

This script checks the version of Matplotlib to see if it matches the version known to have a display issue as described. If the version is the problematic `3.5.0`, it will raise an `AssertionError` and print a stack trace to provide details about the exception context. For any other Matplotlib version, it will indicate that the version is not affected by the described issue. The script will exit with code 0 if the version is not `3.5.0`, demonstrating that the issue has been fixed or is not present in that version.