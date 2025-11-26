Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.contrib import admin
from django.db import models
from django.test import TestCase

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

class Session(models.Model):
    pass

class SessionAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Session, SessionAdmin)

class TestIssue(TestCase):
    def test_issue(self):
        try:
            admin.site.index(None)
        except Exception as e:
            print_stacktrace(e)
            assert False, "Expected no exception"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer.settings")
    import django
    django.setup()
    TestCase.main(module="reproducer")

```
This script defines a `Session` model and a custom `SessionAdmin` that tries to replace the built-in `delete_selected` action. It then registers the admin site and runs a test case that checks if the issue is present.

When run with `python3 reproducer.py`, this script should raise an `AssertionError` with a stack trace indicating the `admin.E130` system check error, which demonstrates the issue. If the issue is fixed, the script should exit with code 0.