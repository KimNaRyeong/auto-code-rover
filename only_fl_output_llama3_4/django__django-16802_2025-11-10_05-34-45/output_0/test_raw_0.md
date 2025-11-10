Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.template import Template, Context
from django.template.defaultfilters import first, last, random
from django.conf import settings

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

def main():
    settings.configure()
    template = Template("{{ list_var|first }}")
    context = Context({"list_var": []})
    try:
        result = template.render(context)
        assert not result, "Expected an empty page"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

To run the reproducer, execute `python3 reproducer.py` in the terminal. If the issue is present, it will print a stack trace and exit with code 1.