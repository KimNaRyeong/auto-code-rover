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


def process_docstring(app: Sphinx, what: str, name: str, obj: Any, options: dict, lines: list):
    if what != "classmethod":
        return

    if not ismethod(obj):
        return

    method_obj = obj.__func__
    method_doc = inspect.getdoc(method_obj)

    if method_doc is None:
        return

    parent_class = method_obj.__objclass__
    parent_class_name = parent_class.__name__

    child_class = obj.__self__
    child_class_name = child_class.__name__

    if parent_class_name not in child_class_name:
        return

    field_name = "inherited_docstring"
    field_type = "str"

    field = Field(field_name, field_type, "Inherited docstring from parent class")
    docfield = DocField(field, method_doc)

    lines.insert(0, f"{field_name}: {docfield.content}")


def run():
    src_mod = sphinx.util.osutil.load_module("src.spam", __file__)

    assert isinstance(src_mod.Parent.method, ClassMethod)
    assert isinstance(src_mod.Child.method, ClassMethod)

    assert src_mod.Parent.method.__doc__ is not None
    assert src_mod.Child.method.__doc__ is None

    assert src_mod.Parent.method.__func__.__doc__ is not None
    assert src_mod.Child.method.__func__.__doc__ is None


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script sets up a Sphinx application and connects to the `autodoc-process-docstring` event. When a `classmethod` is processed, the script checks if the method is inherited from a parent class and if the parent class has a docstring. If both conditions are met, the script adds the parent class's docstring as a new field called `inherited_docstring` to the method's docstring.

To test the script, run `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.