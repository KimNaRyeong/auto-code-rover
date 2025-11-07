Certainly! Below is a standalone Python file named `reproducer.py` designed to replicate the issue described. When executed, it will render a Django template, checking for the double-escaping problem. If the issue is present, it will raise an `AssertionError` and print a detailed stack trace as requested.

```python
import django
from django.conf import settings
from django.template import Template, Context

settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }],
    USE_I18N=True,
)
django.setup()


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


def check_double_escaping():
    template_content = """
{% load i18n %}
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""
    rendered = Template(template_content).render(Context({"title": "<>& Title"}))
    if "&amp;lt;" in rendered:
        raise AssertionError("Title was escaped two times")


if __name__ == "__main__":
    try:
        check_double_escaping()
        print("Issue not found. Exiting with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

Please make sure you have Django installed and correctly setup in your environment before running this script. The script first configures the minimum required Django settings to run, initializes Django, and then proceeds to check for the issue. If the double-escaping issue is present, it will catch the `AssertionError` and print the stack trace as specified.