Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from sphinx.ext import autodoc

def main():
    try:
        class _ClassWithDocumentedInitAndStarArgs:
            """Class docstring."""

            def __init__(self, x: int, *args: int, **kwargs: int) -> None:
                """Init docstring.

                :param x: Some integer
                :param *args: Some integer
                :param **kwargs: Some integer
                """
        sphinx.setup()
        autodoc.generate_doc([_ClassWithDocumentedInitAndStarArgs], autodoc_typehints="description")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```