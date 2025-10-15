```python
# reproducer.py
def main():
    from django.template import Template, Context
    from django.conf import settings

    # Initialize Django to avoid runtime errors
    settings.configure(USE_I18N=True)

    # Define the template content that causes the issue
    template_content = """
{% load i18n %}
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""

    # Render the template with a context that triggers the issue
    rendered = Template(template_content).render(Context({"title": "<>& Title"}))

    # Check if the issue is present
    try:
        assert "&amp;lt;" not in rendered, "> was escaped two times"
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e: Exception):
    # Print a detailed stack trace to understand where the issue occurs
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

if __name__ == "__main__":
    try:
        main()
        exit(0)
    except AssertionError:
        exit(1)
```

This script is designed to reproduce the specific issue with Django's `blocktranslate` template tag leading to double escaping. It initializes the minimum necessary Django settings to render a template, specifically with `USE_I18N=True` to enable internationalization features. 

Upon execution, if the issue is present, an `AssertionError` will be raised, and the script will print a detailed stack trace, indicating where the problem occurred. If the issue is not present (i.e., the assertion passes), the script will exit normally with code 0, indicating the issue's absence or resolution.