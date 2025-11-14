Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.util import inspect

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring


        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        mod = type('mod', (), {'Foo': Foo, 'Bar': Bar})
        autodoc.autodoc(mod)

    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not reproduced")
        exit(0)

if __name__ == "__main__":
    main()
```

This script defines the same classes `Foo` and `Bar` as in your example, then attempts to generate documentation for them using Sphinx's autodoc module. If the issue is present, it should raise an `AssertionError`, which will be caught and a stack trace printed.