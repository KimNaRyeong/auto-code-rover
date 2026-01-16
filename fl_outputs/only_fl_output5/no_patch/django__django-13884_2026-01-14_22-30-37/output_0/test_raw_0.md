```python
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse

# Minimum settings required for Django to run tests
settings.configure(
    SECRET_KEY='a-very-secret-key',
    ROOT_URLCONF=__name__,   # Makes this file also act as the urls.py
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ),
)

# Define a simple view that can be called to initiate the set_language procedure
def set_language(request):
    from django.utils.http import is_safe_url
    from django.utils.translation import LANGUAGE_SESSION_KEY
    from django.http import HttpResponseRedirect

    lang_code = request.POST.get('language', None)
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER'))
    response = HttpResponseRedirect(next_url)
    if lang_code and is_safe_url(url=next_url, allowed_hosts={request.get_host()}):
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response

# URLs configuration, required to make Django serve the `set_language` view
from django.urls import path
urlpatterns = [path('set_language/', set_language, name='set_language')]

# Your test function
def test_set_language_url_params():
    from django.test import RequestFactory
    
    rf = RequestFactory()
    request = rf.post("/set_language/", data={'next': '/someurl/?parameter=some%20%26%20thing'})
    response = set_language(request)
    assert response.url == '/someurl/?parameter=some%20%26%20thing', "URL did not match expected value"

# Function to print the stack trace
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

if __name__ == '__main__':
    django.setup()
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
    try:
        test_set_language_url_params()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("Test passed successfully, no issue detected.")
        raise SystemExit(0)
```