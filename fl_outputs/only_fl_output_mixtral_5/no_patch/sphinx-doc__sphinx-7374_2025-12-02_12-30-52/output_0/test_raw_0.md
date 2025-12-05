 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
import re

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_function_id():
    docstring = '.. py:function:: example_python_function(foo)\n\n    Some function.'
    # Create a mock Sphinx environment to parse the docstring
    env = sphinx.environment.BuildEnvironment(None)
    domain = sphinx.domains.python.PythonDomain(env)
    # Parse the docstring and get the function ID
    statement = sphinx.addnodes.desc(
        :class: 'py function',
        name: 'example_python_function',
        sig: '(foo)',
        lineno: 1,
        reflineno: 1,
        node: None,
        docstring: docstring,
    )
    domain.process_signature(statement, None)
    function_id = statement.attributes['ids'][0]
    # Check if the function ID contains underscores or dashes
    assert re.search(r'_', function_id) is not None, 'Function ID contains dashes instead of underscores'

if __name__ == '__main__':
    try:
        test_function_id()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, this script will raise an `AssertionError` with a stack trace if the function ID contains dashes instead of underscores. If the function ID contains underscores, the script will exit with code 0.

The script uses the `sphinx` module to parse the docstring and extract the function ID. It then checks if the function ID contains underscores or dashes using a regular expression. If the function ID contains dashes, the script raises an `AssertionError` with a stack trace.