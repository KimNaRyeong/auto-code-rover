Here is the reproducer script in Python:
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
    output.seek(0)

    # Check if the issue is present
    html = output.read()
    assert "class=\"compound\"" not in html, "Issue present: missing CSS class for compound keystrokes"

    print_stacktrace(AssertionError("Issue fixed"))

if __name__ == "__main__":
    reproduce_issue()
```
This script uses the `docutils` library to generate HTML output from the given source string. It then checks if the issue is present by searching for the presence of a CSS class named "compound" in the generated HTML. If the issue is not present, it prints a stack trace indicating that the issue has been fixed.

To run the script, save it as `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.