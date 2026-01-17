 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyClass:
    def __init__(self):
        self._my_property: int = 0

def test_autodoc_typehints():
    import sphinx.ext.autodoc
    sphinx.ext.autodoc.typehints = None
    from sphinx.application import Sphinx
    app = Sphinx('test', 'test', source_dir='.', doctree_dir='.', buildername='html')
    app.setup_extension('sphinx.ext.autodoc')
    app.add_autodocumenter(sphinx.ext.autodoc.Autodocumenter)
    app.build(force_all=True)
    with open('_build/html/index.html', 'r') as f:
        content = f.read()
    assert '_my_property: int' not in content, 'Type hints should not be rendered in the output'

if __name__ == '__main__':
    try:
        test_autodoc_typehints()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with a stack trace, indicating that the issue is present. The output should look like this:
```csharp
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    test_autodoc_typehints()
  File "reproducer.py", line 23, in test_autodoc_typehints
    assert '_my_property: int' not in content, 'Type hints should not be rendered in the output'
AssertionError: Type hints should not be rendered in the output
```
If the issue is fixed, the script should exit with code 0, indicating that the test passed.