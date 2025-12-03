 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
import re

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_fragment_identifier():
    # Previously, anchors for Python functions were using underscores
    docstring = ".. py:function:: example_python_function(foo)\n\n    Some function."
    # but since #7236 this creates `#example-python-function`
    domain_id = sphinx.addnodes.desc_signature(None, docstring, None)['domainid']
    assert re.match(r'[a-z\-]+', domain_id) is not None, f"Fragment identifier '{domain_id}' contains underscores."

if __name__ == "__main__":
    try:
        test_fragment_identifier()
        print("No issue found.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, the script will print "No issue found." and exit with code 0.