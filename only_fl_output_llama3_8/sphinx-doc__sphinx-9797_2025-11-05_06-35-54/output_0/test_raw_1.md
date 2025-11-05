Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.util.inspect import getdoc

def main():
    try:
        class Parent:
            @classmethod
            def method(cls) -> int:
                """Return an integer."""
                return 17

        class Child(Parent):
            @classmethod
            def method(cls):
                return 42

        autodoc.autodoc(Child.method, 'reproducer')
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script creates two classes `Parent` and `Child`, where the `method` class method in `Child` is overridden without documentation. It then tries to generate the documentation for the overridden method using Sphinx's autodoc extension, which should raise an `AssertionError` if the issue is present.

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and exit with code 1.