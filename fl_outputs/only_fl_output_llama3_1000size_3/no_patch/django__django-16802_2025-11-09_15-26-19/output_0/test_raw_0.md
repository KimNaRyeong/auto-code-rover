Here is the reproducer script:

```python
import django
from django.template import Template, Engine
from django.conf import settings
from django.test.utils import CaptureHandler
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import first, last, random
from django.template.loader import get_template

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
    engine = Engine()
    template = Template("{{ list_var|random }}")
    
    try:
        result = str(template.render({"list_var": []}))
        if not result:
            raise AssertionError("Expected an error, but got empty string")
    except Exception as e:
        print_stacktrace(e)
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
```

This script sets up a Django template engine and tries to render the `random` filter with an empty list. If no error is raised, it prints an assertion error message.