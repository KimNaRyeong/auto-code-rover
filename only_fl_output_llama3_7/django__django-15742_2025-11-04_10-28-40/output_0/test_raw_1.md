Here is the reproducer script:

```python
import django
from django.template import Template, Context
from django.utils.safestring import mark_safe

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
    try:
        from django.template import Template, Context
    except ImportError as e:
        print_stacktrace(e)
        exit(1)

    template_content = """
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""
    try:
        rendered = Template(template_content).render(Context({"title": "<>& Title"}))
        if "&amp;lt;" in rendered:
            print_stacktrace(AssertionError("Expected '&lt;' not to be escaped twice"))
            exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the issue. If the issue is fixed, it will simply exit with code 0.