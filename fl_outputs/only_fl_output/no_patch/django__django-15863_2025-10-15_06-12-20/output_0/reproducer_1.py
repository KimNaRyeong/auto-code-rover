# reproducer.py
from decimal import Decimal
import sys

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

def setup_django_environment():
    from django import setup
    from django.conf import settings
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]
    settings.configure(TEMPLATES=TEMPLATES)
    setup()

def test_floatformat_precision():
    from django.template import Template, Context
    # Set up a simple Django environment
    setup_django_environment()

    # Test floatformat with a Decimal value
    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': Decimal('42.12345678901234567890')})
    rendered = t.render(c)

    # Verify the output
    expected_output = '42.12345678901234567890'
    assert rendered == expected_output, "floatformat dropped precision for Decimal numbers"

def main():
    try:
        test_floatformat_precision()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with non-zero to indicate failure
        sys.exit(1)

if __name__ == '__main__':
    main()
