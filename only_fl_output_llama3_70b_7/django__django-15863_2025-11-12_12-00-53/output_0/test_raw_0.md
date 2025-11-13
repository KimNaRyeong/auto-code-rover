Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import decimal
from django.template import Template, Context
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

try:
    from django.conf import settings
    from django.template.backends.django import DjangoTemplates

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]
    settings.configure(TEMPLATES=TEMPLATES)
    setup()

    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': decimal.Decimal('42.12345678901234567890')})
    result = t.render(c)

    expected_result = '42.1234567890123457'
    assert result.strip() == expected_result, f"Expected {expected_result}, got {result}"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
```
This script sets up a Django template engine, creates a template with the `floatformat` filter, and renders it with a Decimal value. It then asserts that the result has the expected precision. If the assertion fails, it prints a stack trace of the error using the provided `print_stacktrace` function and exits with code 1.