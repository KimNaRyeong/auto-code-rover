Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication

def reproduce_issue():
    app = SphinxApplication()
    app.build('make-html-warnings', 'html')

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script will create a new Sphinx application, set the source directory to `make-html-warnings` and build the documentation in HTML format. If any warnings are raised during this process, it will catch the exception and print the stack trace.

Please note that you need to have Sphinx installed in your Python environment for this script to work.