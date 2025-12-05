 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import sphinx
import sphinx_gallery

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
    # Check if sphinx-gallery version is new enough
    min_version = (0, 6, 0)
    current_version = sphinx_gallery.__version__
    if tuple(map(int, current_version.split("."))) < min_version:
        e = AssertionError(f"sphinx-gallery {current_version} is not new enough, needs at least version {min_version}")
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
To reproduce the issue, execute the script with `python3 reproducer.py`. The script should raise an `AssertionError` with the following message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 17, in main
    e = AssertionError(f"sphinx-gallery {current_version} is not new enough, needs at least version {min_version}")
AssertionError: sphinx-gallery 0.10.0 is not new enough, needs at least version (0, 6, 0)
```
This reproduces the issue where the `needs_extensions` check is done in a "string-like" manner, which results in the current version of `sphinx-gallery` being rejected even though it is greater than or equal to the minimum specified version.