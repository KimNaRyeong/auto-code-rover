# reproducer.py

def setup_django_environment():
    import django
    from django.conf import settings

    settings.configure(
        USE_I18N = True,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
        ],
        # Dummy database configurations, required for initializing apps
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        # Necessary to avoid issues related to Sites framework when running without a full project
        SITE_ID=1,
        # Ensuring templates are loaded correctly
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
    )
    django.setup()


def main():
    from django.template import Template, Context

    # Define the template content that causes the issue
    template_content = """
{% load i18n %}
{% blocktranslate asvar the_title %}The title is {{ title }}.{% endblocktranslate %}
<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
"""

    # Render the template with a context that might trigger the issue
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
    setup_django_environment()
    try:
        main()
        exit(0)  # Exit with code 0 if no exception is raised, indicating the issue is fixed.
    except AssertionError:
        exit(1)  # Exit with code 1 if AssertionError is raised, indicating the presence of the issue.
