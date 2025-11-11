Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc

def main():
    try:
        with open('test.cpp', 'w') as f:
            f.write('''
.. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)
''')
        from sphinx.application import SphinxApplication
        app = SphinxApplication()
        app.build(['.'], ['html'])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected error"

if __name__ == "__main__":
    main()
```

This script attempts to write the given reST code to a file named 'test.cpp' and then runs Sphinx's build function with the current directory as input. If an error occurs during this process (which should be the case due to the presence of the spaceship operator), it prints a stack trace and raises an `AssertionError`.