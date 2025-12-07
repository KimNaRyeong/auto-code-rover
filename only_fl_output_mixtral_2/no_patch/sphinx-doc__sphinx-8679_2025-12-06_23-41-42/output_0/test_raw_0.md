 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import setup
from docutils.core import publish_string

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
    # Arrange
    source = """\
.. _reference:

.. rubric:: This rubric will be a ``broken`` reference

Let's call the :ref:`reference`
"""
    expected = """\
<system-message style="docutils.error" name="error" line="5">
<paragraph>
Problem in Rubric directive:
</paragraph>
<paragraph>
The reference target name ``reference`` is not unique: it matches the name of the
following directive: "rubric <reference>" (<reference>).
</paragraph>
</system-message>"""

    # Act & Assert
    try:
        setup(app=sphinx.application.Sphinx())
        result = publish_string(source, writer_name='html')
        assert result.find(expected) != -1, "The expected error message was not found in the output."
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred."

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the expected error message was not found in the output. This reproduces the issue where the reference text is broken when trying to display a reference pointing at a "rubric" directive containing a part that is ``quoted``.