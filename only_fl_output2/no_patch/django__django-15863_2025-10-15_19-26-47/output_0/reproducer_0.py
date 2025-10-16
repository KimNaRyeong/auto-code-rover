# reproducer.py
def main():
    from decimal import Decimal
    from django import setup
    from django.conf import settings
    from django.template import Template, Context

    # Setup Django to use the default settings
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]
    settings.configure(TEMPLATES=TEMPLATES)
    setup()

    # Template that uses the floatformat filter
    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': Decimal('42.12345678901234567890')})

    # Render the template
    rendered = t.render(c)

    # Check if the rendered output matches the expected precision
    expected_output = "42.12345678901234567890"
    try:
        assert rendered.strip() == expected_output, f"Output {rendered} does not match expected {expected_output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

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
    try:
        main()
        exit(0)  # Issue is fixed, exit with code 0
    except Exception as e:
        exit(1)  # An exception occurred, indicating the issue is present
