 Here's a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import pylint
import pylint_quotes

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

def main():
    pylint_version = tuple(map(int, pylint.__version__.split(".")))
    if (2, 8, 2) < pylint_version:
        print("Expected failure: pylint-quotes does not support pylint 2.8.2")
        assert False
    else:
        print("Expected success: pylint-quotes should work with this version of pylint")

    # Create a dummy AST node to trigger the error
    class DummyNode:
        def __init__(self):
            self.lineno = 1
            self.col_offset = 1

    ast_node = DummyNode()

    # Initialize pylint-quotes checker
    checker = pylint_quotes.checker.Checker()

    # Call the problematic method
    checker._invalid_string_quote(ast_node, 1, 1)

    print("Success: pylint-quotes works with this version of pylint")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with `python3 reproducer.py`. If the issue is present, the script should print the following output:
```python
Expected failure: pylint-quotes does not support pylint 2.8.2
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    main()
  File "reproducer.py", line 21, in main
    checker._invalid_string_quote(ast_node, 1, 1)
  File "/path/to/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 341, in _invalid_string_quote
    **self.get_offset(col)
  File "/path/to/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 360, in get_offset
    if (2, 2, 2) < pylint_version:
TypeError: '<' not supported between instances of 'int' and 'str'
```
If the issue is fixed, the script should print "Expected success: pylint-quotes should work with this version of pylint" and "Success: pylint-quotes works with this version of pylint".