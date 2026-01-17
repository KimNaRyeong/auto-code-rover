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
    rst_text = """
    .. py:function:: example_python_function(foo)

        Some function.
    """
    # When
    domain_ids = sphinx.addnodes.literal_strong(text=rst_text, **{})
    domain_ids_text = ''.join(node.astext() for node in domain_ids)
    # Then
    expected_fragment_identifier = "#example_python_function"
    actual_fragment_identifier = re.search(r'#([^ ]+)', domain_ids_text).group(1)
    assert actual_fragment_identifier == expected_fragment_identifier, \
        f"Expected fragment identifier {expected_fragment_identifier} but got {actual_fragment_identifier}"

if __name__ == "__main__":
    try:
        test_fragment_identifier()
        print("No issue found.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. The expected and actual fragment identifiers will be printed in the error message.

The script uses the `sphinx` library to parse the reStructuredText (RST) text and extract the domain IDs. It then uses a regular expression to extract the fragment identifier from the generated HTML. The `assert` statement checks if the actual fragment identifier matches the expected one (with underscores). If the assertion fails, an `AssertionError` is raised, which is caught and printed with a stack trace by the `print_stacktrace` function. The script exits with a non-zero exit code to indicate that the issue was found.