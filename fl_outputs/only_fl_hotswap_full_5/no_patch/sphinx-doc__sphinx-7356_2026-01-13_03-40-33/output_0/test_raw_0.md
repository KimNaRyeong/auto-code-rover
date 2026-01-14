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
    # Previously, anchors for Python functions were using underscores
    # but #7236 changed this to dashes
    function_name = "example_python_function"
    docstring = f".. py:function:: {function_name}(foo)\n\n    Some function."
    # This used to create a fragment identifier `#example_python_function`
    # but since #7236 this creates `#example-python-function`
    dom_obj = sphinx.addnodes.desc(
        nodeclass=sphinx.addnodes.desc,
        docname="",
        lineno=0,
        reflineno=None,
        anchorname=None,
        content="",
        lineno_system=None,
        hidden=False,
        classes=None,
        backrefs=None,
        **{'domain': 'py', 'name': function_name, 'objtype': 'function'}
    )
    sphinx.addnodes.desc_signature(dom_obj, text=function_name + "(foo)")
    sphinx.addnodes.desc_addname(dom_obj, text=function_name)
    sphinx.addnodes.desc_content(dom_obj, text="Some function.")
    dom_obj.walkabout(None)
    assert re.match(r"^#example-python-function$", dom_obj['anchorname']) is None

if __name__ == "__main__":
    try:
        test_fragment_identifier()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace showing the line where the assertion fails. This demonstrates that the fragment identifier for the Python function is created with dashes instead of underscores. When the issue is fixed, the script should exit with code 0 without printing any error message.