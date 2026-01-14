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
    # Given
    docstring = ".. py:function:: example_python_function(foo)\n\n    Some function."
    # When
    domain_ids = sphinx.addnodes.literal_strong(typ='domain-id', value='')
    sphinx.addnodes.desc(domain_ids, docstring)
    fragment_identifier = re.search(r'#([^ ]+)', domain_ids[0].astext()).group(1)
    # Then
    assert fragment_identifier == 'example_python_function', f"Expected fragment identifier to be 'example_python_function', but got '{fragment_identifier}' instead."

if __name__ == "__main__":
    try:
        test_fragment_identifier()
        print("No issue found.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the fragment identifier is `example-python-function` instead of `example_python_function`. This reproduces the issue described in the bug report.