import sys
from django.urls import path, resolve
from django.http import HttpResponse
from django.views import View

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

class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, world!")

urlpatterns = [
    path('home', HomeView)
]

def main():
    try:
        # Try to access the URL pattern
        from django.core.handlers.wsgi import WSGIRequest
        from django.test.client import RequestFactory
        rf = RequestFactory()
        request = rf.get('/home')
        resolve('/home')(request)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error should be raised when forgetting to call .as_view() on a CBV"

if __name__ == "__main__":
    main()
