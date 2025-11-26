import django
from django.urls import path
from django.http import HttpResponse
from django.views import View

class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, world!")

urlpatterns = [
    path('home', HomeView)
]

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

try:
    from django.core.handlers.wsgi import WSGIRequest
    request = WSGIRequest({'wsgi.input': '', 'REQUEST_METHOD': 'GET', 'PATH_INFO': '/home'})
    response = django.urls.resolvers.get_resolver(None).resolve('/home')(request)
    assert False, "Expected an error to be raised"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is still present")
