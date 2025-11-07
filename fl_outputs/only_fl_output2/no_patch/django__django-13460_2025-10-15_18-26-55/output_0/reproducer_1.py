# reproducer.py
import sys

def setup_django():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        USE_I18N=True,
        LANGUAGE_CODE='ru',
        LANGUAGES=(('ru', 'Russian'),),
    )

    import django
    django.setup()

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    from django.template import Context, Template
    from django.utils.translation import activate

    # Activate Russian locale
    activate('ru')

    template_string = '''
    {% load i18n %}
    {% blocktrans count counter=distance|floatformat:0 %}
        {{ counter }} mile away
    {% plural %}
        {{ counter }} miles away
    {% endblocktrans %}
    '''

    context = Context({'distance': 1.5})

    try:
        template = Template(template_string)
        rendered = template.render(context)
        if 'миль' not in rendered:
            raise AssertionError("Localization issue was not reproduced - failed to render the correct plural form.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error encountered during template rendering.")

if __name__ == '__main__':
    try:
        setup_django()
        reproduce_issue()
        print("Test completed successfully without reproducing the issue.")
    except AssertionError as error:
        print_stacktrace(error)
        sys.exit(1)
    except Exception as unexpected_error:
        print("An unexpected error occurred:", unexpected_error)
        sys.exit(1)
