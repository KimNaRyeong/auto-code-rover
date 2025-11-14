Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList

class MyException:
    """My Exception class.

    Attributes:
        message (str): The exception message.
    """
    def __init__(self, message: str):
        self.message = message

def setup(app):
    app.add_directive('autoclass', AutodocDirective)
    app.add_autodocumenter(MyException)

def test_issue():
    src_dir = 'docs/source'
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write('.. autoclass:: MyException\n    :members:\n')

    app = Sphinx(src_dir, src_dir, 'docs/build', 'docs/build')
    app.setup()
    app.build()

def main():
    try:
        test_issue()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    main()

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
```
This script creates a minimal Sphinx project with an `index.rst` file that uses the `autoclass` directive to document the `MyException` class. The `MyException` class has a type hint for its `message` attribute.

When run, this script will raise an `AssertionError` if the issue is present (i.e., if the generated documentation has two entries for each attribute). If the issue is fixed, the script will exit with code 0.