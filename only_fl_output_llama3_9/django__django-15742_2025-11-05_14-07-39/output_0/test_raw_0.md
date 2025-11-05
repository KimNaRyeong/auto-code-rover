Here is the reproducer script:

```python
import django
from django.template import Template, Context

def main():
    try:
        template_content = """
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""
        rendered = Template(template_content).render(Context({"title": "<>& Title"}))
        assert "&amp;lt;" not in rendered, ">& was escaped two times"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue is fixed. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    django.setup()
    main()

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

```

You can run this script using `python3 reproducer.py`.