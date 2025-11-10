Here is the reproducer script:

```python
import django
from django.template import Template, Context
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        settings_module = 'polls.settings'
        django.setup()
        template = Template('{{ list_var|random }}')
        context = Context({'list_var': []})
        result = str(template.render(context))
        if not result:
            raise AssertionError("Expected an error, but got empty string")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a Django environment and tries to render a template with the `random` filter on an empty list. If the rendering does not raise an error, the script raises an assertion error.