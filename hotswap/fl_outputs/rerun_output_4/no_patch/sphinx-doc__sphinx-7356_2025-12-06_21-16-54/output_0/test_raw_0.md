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

def test_function_id():
    docstring = '.. py:function:: example_python_function(foo)\n\n    Some function.\n'
    domain_ids = sphinx.addnodes.desc.desc_signature(None, '', docstring, 0).asdom().attrib['ids']
    assert len(domain_ids) == 1
    domain_id = domain_ids[0]
    assert re.match(r'^example-python-function$', domain_id) is not None

if __name__ == '__main__':
    try:
        test_function_id()
        print('The issue is fixed.')
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. The script will exit with code 1 if the issue is present and with code 0 if the issue is fixed.

The `test_function_id` function tests the behavior of the `sphinx.addnodes.desc.desc_signature` function, which is responsible for generating the domain IDs for Python functions. The function asserts that the domain ID for the example function contains dashes instead of underscores. If the assertion fails, an `AssertionError` is raised and caught by the `except` block, which prints a stack trace and exits with code 1. If the assertion passes, the script prints a success message and exits with code 0.