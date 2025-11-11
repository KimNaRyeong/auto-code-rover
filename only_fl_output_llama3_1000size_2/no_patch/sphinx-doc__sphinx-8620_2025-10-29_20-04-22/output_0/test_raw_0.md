Here is the reproducer script:

```python
import docutils.core
from io import StringIO

def reproduce_issue():
    source = r"""
:kbd:`A`

:kbd:`Shift+X`
"""

    output = StringIO()
    docutils.core.publish_string(source, writer_name='html', outputfile=output)

    if not output.getvalue().startswith('<body><div class="docutils literal notranslate">'):
        raise AssertionError("Expected HTML header")

    html = output.getvalue()

    # Check for compound keystroke
    if '<kbd class="kbd docutils literal notranslate">' in html and '+</kbd>' in html:
        if not 'class="compound"' in html:
            raise AssertionError("Compound keystroke expected to have a CSS class")

    print_stacktrace(AssertionError("Issue reproduced successfully"))

if __name__ == "__main__":
    reproduce_issue()
```

This script uses the `docutils` library to generate HTML from the given input. It checks if the generated HTML contains the expected structure and classes for single keystrokes and compound keystrokes. If the issue is present, it raises an `AssertionError` with a stack trace.