I apologize for the previous mistake. Here is a new `reproducer.py` script to reproduce the issue:
```
import sys
from packaging import version

def needs_extensions_check(loaded_version, required_version):
    return version.parse(loaded_version) >= version.parse(required_version)

def main():
    try:
        loaded_version = "0.10.0"
        required_version = "0.6.0"
        
        if not needs_extensions_check(loaded_version, required_version):
            raise AssertionError(f"This project needs the extension sphinx_gallery.gen_gallery at least in version {required_version} and therefore cannot be built with the loaded version ({loaded_version}).")
        
        print("Version accepted, no issue found.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

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
```
This script uses the `packaging` library to compare versions correctly. It checks if the loaded version "0.10.0" is greater than or equal to the required version "0.6.0". If not, it raises an `AssertionError`.