Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from sphinx.ext import autodoc

def main():
    try:
        class Foo:
            """docstring"""
            attr1: int  #: docstring


        class Bar(Foo):
            """docstring"""
            attr2: str  #: docstring

        from sphinx.ext import autodoc
        from sphinx.util import inspect

        mod = sys.modules["example"]
        obj = mod.Bar

        def visit_member(node: nodes.Node) -> None:
            if node.children[0].text == "attr1":
                raise AssertionError("Bar.attr1 is not documented")

        inspect.autodoc_visit_member(visit_member)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

This script should be able to reproduce the issue by checking if `Bar.attr1` is documented. If it's not, an `AssertionError` will be raised and a stack trace will be printed.