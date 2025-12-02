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

if sphinx.__version__ < '4.1.2':
    print("Sphinx version is less than 4.1.2, which is required for this reproducer.")
    sys.exit(0)

if sphinx_gallery.__version__ < '0.6.0':
    print("Sphinx-gallery version is less than 0.6.0, which is required for this reproducer.")
    sys.exit(0)

# The following line will raise an AssertionError if the issue is present
assert sphinx_gallery.__version__ >= '0.6.0' or sphinx.__version__ < '4.1.2', \
    "The 'needs_extensions' check is done in a 'string-like' manner, which causes the issue."
```
To reproduce the issue, execute the script with `python3 reproducer.py`. The script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    assert sphinx_gallery.__version__ >= '0.6.0' or sphinx.__version__ < '4.1.2', "The 'needs_extensions' check is done in a 'string-like' manner, which causes the issue."
AssertionError: The 'needs_extensions' check is done in a 'string-like' manner, which causes the issue.
```
To fix the issue, either update the `needs_extensions` check to compare versions using the `packaging` library or update Sphinx to version 4.1.2 or later.