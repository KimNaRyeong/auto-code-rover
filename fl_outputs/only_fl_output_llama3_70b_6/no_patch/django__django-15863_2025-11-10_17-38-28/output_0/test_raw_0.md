Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import decimal
from django.template import Template, Context

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

try:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        },
    ]
    from django.conf import settings
    settings.configure(TEMPLATES=TEMPLATES)
    from django import setup
    setup()

    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': decimal.Decimal('42.12345678901234567890')})
    result = t.render(c)

    expected_result = '42.1234567890123457'
    assert result.strip() == expected_result, f"Expected {expected_result}, got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```
This script can be executed by running `python3 reproducer.py` in the root directory of the project. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.