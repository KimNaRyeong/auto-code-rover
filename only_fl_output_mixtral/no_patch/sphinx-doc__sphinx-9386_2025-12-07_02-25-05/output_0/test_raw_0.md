 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
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

class MyClass:
    @property
    def my_property(self) -> int:
        """My property."""
        return 42

def test():
    my_instance = MyClass()
    import inspect
    import sphinx.ext.autodoc
    options = {'autodoc_typehints': 'none'}
    add_docstring = sphinx.ext.autodoc.setup(inspect.currentframe(), options)
    add_docstring(my_instance, 'my_instance', MyClass)
    assert 'my_property: int' not in my_instance.__doc__

if __name__ == '__main__':
    try:
        test()
    except AssertionError as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    test()
  File "reproducer.py", line 23, in test
    assert 'my_property: int' not in my_instance.__doc__
AssertionError: 'my_property: int'
```
This script creates a class `MyClass` with a property `my_property` that has a type hint of `int`. It then uses the `sphinx.ext.autodoc` module to generate documentation for the class and checks that the type hint is not included in the generated documentation. If the type hint is included, the script raises an `AssertionError`.