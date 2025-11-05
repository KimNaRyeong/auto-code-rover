Here is the reproducer script in a code block:

```python
import smtplib
from django.core.mail import mail_managers, BadHeaderError
from django.conf import settings
from django.utils.log import print_stacktrace

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

settings.configure()

try:
    settings.MANAGERS = ['one@example.com', 'two@example.com']
    mail_managers('Subject', 'Message')
except BadHeaderError as e:
    assert False, "Expected BadHeaderError"
    print_stacktrace(e)
    exit(1)
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable and then configures Django settings. It then attempts to set the `MANAGERS` setting to an improper format and call `mail_managers()` with a subject and message. If an exception is raised (which should be a `BadHeaderError`), it asserts that this is not expected, prints the stack trace, and exits with code 1.