# reproducer.py
import django
from django.template import Context, Engine
from django.utils.translation import gettext as _

def setup_django_environment():
    from django.conf import settings
    settings.configure(
        USE_I18N=True,
        LANGUAGE_CODE='ru',
        BASE_DIR=".",
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [],
            },
        }],
    )
    django.setup()

def mock_translation_gettext(singular, plural, n):
    if n == 1:
        return "На расстоянии %(counter)s мили"
    else:
        return "На расстоянии %(counter)s миль"

def render_template_with_trans_block(distance):
    engine = Engine.get_default()
    template = engine.from_string(
        "{% load i18n %}"
        "{% blocktrans count counter=distance|floatformat:0 %}"
        "{{ counter }} mile away"
        "{% plural %}"
        "{{ counter }} miles away"
        "{% endblocktrans %}"
    )
    return template.render(Context({'distance': distance}))

def main():
    setup_django_environment()

    distance_in_miles = 1.5  # A test distance

    try:
        result = render_template_with_trans_block(distance_in_miles)
        assert "На расстоянии 2 мили" in result, "Distance not correctly formatted in plural form."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The template rendering failed due to a string formatting error.")

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

if __name__ == "__main__":
    main()
