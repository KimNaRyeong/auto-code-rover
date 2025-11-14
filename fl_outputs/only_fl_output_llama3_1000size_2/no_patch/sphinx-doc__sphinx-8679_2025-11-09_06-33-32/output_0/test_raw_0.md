Here is the reproducer script:

```python
import sys
from sphinx.application import SphinxApplication
from sphinx.util.nodes import setup_sphinx_directives

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    app = SphinxApplication()
    setup_sphinx_directives(app.builder, app.config)

    try:
        from sphinx.util.nodes import get_source_text
        source_text = get_source_text(app.builder, "reference")
        if not source_text.startswith(".. rubric:: This rubric will be a ``broken`` reference"):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    try:
        from sphinx.util.nodes import get_source_text
        source_text = get_source_text(app.builder, "reference")
        if source_text.startswith(".. rubric:: This rubric will be a ``broken`` reference"):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```