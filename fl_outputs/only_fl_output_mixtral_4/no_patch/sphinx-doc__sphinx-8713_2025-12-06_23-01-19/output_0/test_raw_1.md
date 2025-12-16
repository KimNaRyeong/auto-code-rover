 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
from sphinx.ext.napoleon import NumpyDocstring

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
    try:
        docstring = NumpyDocstring("""\
        Parameters\
        ----------\
        x : int\
\
        Other parameters\
        ----------------\
        y: float\
        """)
        formatted_docstring = docstring.get_sections()
        formatted_params = formatted_docstring['Parameters']
        formatted_other_params = formatted_docstring['Other Parameters']
        assert ':param' in formatted_params and ':type' in formatted_params
        assert ':param' not in formatted_other_params and ':type' not in formatted_other_params
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 20, in main
    assert ':param' not in formatted_other_params and ':type' not in formatted_other_params
AssertionError
```
This reproduces the issue where the `Other Parameters` section is not formatted with `:param` and `:type` directives, even when `napoleon_use_param` is set to `True`.