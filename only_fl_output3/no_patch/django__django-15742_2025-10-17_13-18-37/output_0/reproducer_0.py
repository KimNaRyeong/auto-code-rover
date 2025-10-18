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

def main():
    from django.conf import settings

    settings.configure(
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        USE_I18N=True,
        # Assuming you have the 'en' locale activated or any other locales you plan to use.
        LANGUAGES=[('en', 'English')],
    )

    import django
    django.setup()

    from django.template import Template, Context

    template_content = """
{% load i18n %}
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""

    rendered = Template(template_content).render(Context({"title": "<>& Title"}))

    try:
        assert "&amp;lt;" not in rendered, "Title was escaped two times"
        print("The issue is fixed. No AssertionError was raised.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
