Here is the reproducer script:

```python
import sphinx
from sphinx.application import SphinxApplication
from sphinx.ext import needs_extensions

def reproduce_issue():
    app = SphinxApplication()
    try:
        app.builder.config['needs_sphinx_gallery'] = '0.6.0'
        app.builder.config['sphinx_gallery_version'] = '0.10.0'
        app.builder.check_all_toc()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a Sphinx application, sets the minimum required version of sphinx-gallery to 0.6.0 and the actual installed version to 0.10.0, then attempts to check all TOC entries. If an exception is raised, it prints the stack trace and raises an `AssertionError` to indicate that the issue has been reproduced.

To run this script, save it in a file named `reproducer.py`, navigate to the root directory of the project, and execute it with Python 3: `python3 reproducer.py`.