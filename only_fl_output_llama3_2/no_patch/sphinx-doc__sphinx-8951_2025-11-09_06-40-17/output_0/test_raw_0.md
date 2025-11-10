Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc

def main():
    try:
        sphinx.ext.autodoc.process_doc('''
.. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)
''')
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected error"

if __name__ == "__main__":
    main()
```

This script attempts to process the given reST code using Sphinx's autodoc extension. If an error occurs during processing (which should be the case due to the presence of the spaceship operator), it prints a stack trace and raises an `AssertionError`.