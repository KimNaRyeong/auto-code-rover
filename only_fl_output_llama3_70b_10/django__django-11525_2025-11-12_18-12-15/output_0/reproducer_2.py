import os
from django.conf import settings
from django.core import mail

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

# Set the MANAGERS setting to an improper format
settings.configure(MANAGERS=['one@example.com', 'two@example.com'])

try:
    mail.mail_managers("Subject", "Message")
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected exception due to improper MANAGERS setting"
else:
    print("No exception raised, issue is fixed")
    exit(0)
