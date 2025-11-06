Here is the standalone Python file `reproducer.py` to reproduce the issue:

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
    t = Template('{{ value|floatformat:20 }}')
    c = Context({'value': decimal.Decimal('42.12345678901234567890')})
    try:
        print(t.render(c))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script will attempt to render a template with a `floatformat` filter applied to a decimal value. If the issue is present, it will catch the exception and print the stack trace using the provided function.