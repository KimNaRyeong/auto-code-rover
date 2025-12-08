 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LogoutView
from django.test.client import Client
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        redirect_to = super().get_next_page()
        if redirect_to == self.request.GET.get('next'):
            return redirect_to
        return settings.LOGOUT_REDIRECT_URL
