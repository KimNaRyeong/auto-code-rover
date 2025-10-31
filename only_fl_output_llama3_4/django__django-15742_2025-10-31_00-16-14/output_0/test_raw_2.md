Here is the reproducer script:

```python
import django
from django.template import Template, Context

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
    template_content = """
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""
    try:
        rendered = Template(template_content).render(Context({"title": "<>& Title"}))
        assert "&amp;lt;" not in rendered, "> was escaped two times"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
```

This script sets up a Django environment using `django.setup()`, then attempts to render the given template with the specified context. If the assertion fails, it prints the stack trace and exits with code 1.

Please note that you need to have Django installed in your Python environment for this script to work.