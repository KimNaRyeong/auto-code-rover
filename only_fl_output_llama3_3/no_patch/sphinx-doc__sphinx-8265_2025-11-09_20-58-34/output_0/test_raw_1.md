Here is the reproducer script:

```python
import sphinx
from docutils import nodes, utils

def add_lines(self, lines, color=(1, 1, 1), width=5, label=None, name=None):
    pass

if __name__ == "__main__":
    try:
        from pyvista import plotter
        plotter.add_lines((0, 0, 0))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

print("Issue not reproduced. Everything looks fine.")
```

This script tries to reproduce the issue by importing `pyvista` and calling its `add_lines` method with default arguments. If the issue is present, it should raise an `AssertionError` and print the stack trace.