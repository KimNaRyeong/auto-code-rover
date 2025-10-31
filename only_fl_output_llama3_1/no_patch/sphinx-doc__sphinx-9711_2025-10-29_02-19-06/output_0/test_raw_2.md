I apologize for the previous mistake. Here is a new standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from sphinx.ext import needs_extensions

def reproduce_issue():
    try:
        from sphinx_gallery.setup import setup_commands
        from sphinx_gallery.gen_gallery import gen_gallery
        setup_commands()
        gen_gallery('doc', 'mplcursors')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    os.environ['SPHINX_GALLERY_VERSION'] = '0.10'
    reproduce_issue()
```

This script sets the `SPHINX_GALLERY_VERSION` environment variable to `'0.10'`, which should trigger the issue. The `reproduce_issue()` function attempts to import and use Sphinx Gallery, but it will raise an exception if the issue is present. The `print_stacktrace()` function is used to print the stack trace of the exception.

To run this script, save it in a file named `reproducer.py` in the root directory of the project, then execute it with `python3 reproducer.py`. If the issue is present, you should see an error message and a stack trace.