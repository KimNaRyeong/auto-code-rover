The issue is that the `settings.configure()` function does not actually configure Django's settings. It only sets up a temporary configuration for the duration of the script.

To reproduce this issue, we need to use the `django.setup()` function instead:

```python
import os
from django.core import settings
from django.template.loader import get_template
import traceback
import sys

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
    settings.configure({
        'TEMPLATES': [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(os.getcwd(), 'templates')],
                'APP_DIRS': True,
                'OPTIONS': {
                    'cache_templates': True, 
                    'autoreload': True
                }
            }
        ]
    })

    try:
        from django.template.loader import get_template
        settings.setup()
        template = get_template('test.html')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up a Django settings configuration with the cached template loader and autoreload enabled. It then attempts to load a template, which should fail if the issue is present. The `print_stacktrace` function is used to print the stack trace of the exception.