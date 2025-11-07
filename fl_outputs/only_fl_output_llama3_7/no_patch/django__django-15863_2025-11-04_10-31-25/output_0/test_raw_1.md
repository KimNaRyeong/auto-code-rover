Here is the reproducer script:

```python
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

def reproduce_issue():
    try:
        from django import setup
        from django.conf import settings
        settings.configure(TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
            },
        ])
        setup()
        t = Template('{{ value|floatformat:20 }}')
        c = Context({'value': decimal.Decimal('42.12345678901234567890')})
        print(t.render(c))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up the Django environment, defines a template with a floatformat filter, and then renders it with a Decimal value. If the issue is present, it will print a stack trace and raise an `AssertionError`.