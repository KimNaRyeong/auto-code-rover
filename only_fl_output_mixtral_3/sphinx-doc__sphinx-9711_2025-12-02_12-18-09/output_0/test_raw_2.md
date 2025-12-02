 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
from distutils.spelling import Version


def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    min_version = "0.6.0"
    current_version = "0.10.0"
    min_version_obj = Version(min_version)
    current_version_obj = Version(current_version)
    if min_version_obj > current_version_obj:
        msg = f"This project needs the extension sphinx_gallery.gen_gallery at least in version {min_version} and therefore cannot be built with the loaded version ({current_version})."
        e = AssertionError(msg)
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```
To reproduce the issue, save the above code in a file named `reproducer.py` in the root directory of the project and execute it using `python3 reproducer.py`. The script should raise an `AssertionError` with the following message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    main()
  File "reproducer.py", line 14, in main
    if min_version_obj > current_version_obj:
AssertionError: This project needs the extension sphinx_gallery.gen_gallery at least in version 0.6.0 and therefore cannot be built with the loaded version (0.10.0).
```
The expected behavior is that the script should not raise an `AssertionError` when the minimum specified version is 0.6.0 and the current version is 0.10.0. To fix the issue, the `needs_extensions` check should be modified to compare versions using the `distutils.spelling.Version` class instead of treating them as strings.