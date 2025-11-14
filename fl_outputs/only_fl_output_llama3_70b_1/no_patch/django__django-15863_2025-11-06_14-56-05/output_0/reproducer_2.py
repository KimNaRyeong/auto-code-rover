import decimal
from django.conf import settings
from django.template import Template, Context
import django

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    },
]

settings.configure(TEMPLATES=TEMPLATES)
django.setup()

try:
    decimal.getcontext().prec = 30
    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': decimal.Decimal('42.12345678901234567890')})
    result = t.render(c)
    assert result.strip() == '42.12345678901234567890', "Float format filter drops precision"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
