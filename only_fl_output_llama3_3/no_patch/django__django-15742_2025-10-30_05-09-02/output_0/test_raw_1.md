Here is the standalone Python file `reproducer.py` to reproduce the issue:

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
    template_content = """
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title|safe }}</title>
<meta name="description" content="{{ the_title|safe }}">
"""
    try:
        rendered = Template(template_content).render(Context({"title": mark_safe("<>& Title")}))
        assert "&amp;lt;" not in rendered, "> was escaped two times"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, simply execute `python3 reproducer.py` from the command line. If the issue is present, it will raise an `AssertionError`, print a stack trace of the issue, and exit with code 1.