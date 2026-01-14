 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(_('name'), max_length=25