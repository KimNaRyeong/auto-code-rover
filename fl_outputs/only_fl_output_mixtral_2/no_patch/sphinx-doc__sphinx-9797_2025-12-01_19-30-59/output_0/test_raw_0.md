 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from typing import Any, Callable, Type

import sphinx
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassMethod
from sphinx.util.docfields import Field, DocField
from sphinx.util.inspect import ismethod


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def setup(app: Sphinx):
    app.connect("autodoc-process-docstring", process_docstring)


def process_docstring(
    app: Sphinx, what: str, name: str, obj: Any, options: dict, lines: list
):
    if what == "classmethod" and ismethod(obj) and obj.__doc__ is None:
        parent_class = get_parent_class(obj.__self__.__class__)
        if parent_class is not None and hasattr(parent_class, name):
            parent_method = getattr(parent_class, name)
            if parent_method.__doc__ is not None:
                lines[:0] = [parent_method.__doc__]


def get_parent_class(cls: Type) -> Type | None:
    for base in cls.__bases__:
        if base is not object:
            return base
    return None


if __name__ == "__main__":
    sys.path.insert(0, "..")
    app = sphinx.application.Sphinx(srcdir=".", confdir=".", outdir=".", doctreedir=".")
    app.setup_extension("sphinx.ext.autodoc")
    app.setup_extension("reproducer")
    app.build(force_all=True)

    obj = getattr(getattr(app.env.app.object_types["module"], "spam"), "Child")
    method = getattr(obj, "method")

    if not isinstance(method, ClassMethod):
        raise AssertionError("Expected ClassMethod, got: " + str(type(method)))

    if method.__doc__ is None:
        raise AssertionError(
            "Expected docstring to be inherited, but got None."
        )

    print("No issues found.")
```
This script modifies the `autodoc-process-docstring` event to inherit the docstring from the parent class if the child class method does not have a docstring.

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will print "No issues found." and exit with code 0.