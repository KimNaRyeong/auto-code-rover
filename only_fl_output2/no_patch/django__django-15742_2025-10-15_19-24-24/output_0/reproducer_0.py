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
