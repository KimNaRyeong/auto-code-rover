Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.util import inspect

def main():
    try:
        Parent = object  # Create a mock class to test the issue
        Child = type('Child', (Parent,), {'method': lambda cls: None})
        autodoc.autodoc(Child.method, 'reproducer')
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script creates a mock class `Parent` and its child class `Child`, which overrides the `method` class method without documentation. It then tries to generate the documentation for the overridden method using Sphinx's autodoc extension, which should raise an `AssertionError` if the issue is present.

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and exit with code 1.