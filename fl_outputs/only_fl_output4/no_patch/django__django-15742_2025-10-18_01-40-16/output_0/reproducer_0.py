# reproducer.py

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
    from django.template import Template, Context

    settings.configure(
        # Minimal configuration necessary for Django templates to work.
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        }],
        USE_I18N = True,  # Enable Django's internationalization system
        # Include necessary apps
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ]
    )
    
    # Import and set up Django after configuring settings.
    import django
    django.setup()
    
    template_content = """
    {% load i18n %}
    {% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
    <title>{{ the_title }}</title>
    <meta name="description" content="{{ the_title }}">
    """
    try:
        rendered = Template(template_content).render(Context({"title": "<>& Title"}))
        assert "&amp;lt;" not in rendered, "> was escaped two times"
        print("No issues found! The test passed successfully.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
