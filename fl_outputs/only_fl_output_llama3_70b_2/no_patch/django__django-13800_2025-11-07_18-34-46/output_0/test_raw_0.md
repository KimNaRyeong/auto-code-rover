Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
import os
from django.contrib.messages import get_messages
from django.http import HttpResponse

def view(request):
    request.session['messages'] = ['123\\"NOTRECEIVED"']
    messages = get_messages(request)
    response = HttpResponse('Test')
    for message in messages:
        response.set_cookie('messages', message)
    return response

try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer_settings'
    import django
    django.setup()
    request = django.http.HttpRequest()
    view(request)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present: Not RFC 6265 compliant cookies in contrib.messages")
else:
    print("Issue is fixed!")
```
This script sets up a Django environment, defines a simple view that sets a cookie with an invalid value (according to RFC 6265), and then tries to access the view. If the issue is present, it should raise an `AssertionError` with a stack trace of the exception. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.

Note that you'll need to create a `reproducer_settings.py` file in the same directory as this script, with the following contents:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'django.contrib.messages',
]
```
This sets up a minimal Django project with the `messages` app enabled.