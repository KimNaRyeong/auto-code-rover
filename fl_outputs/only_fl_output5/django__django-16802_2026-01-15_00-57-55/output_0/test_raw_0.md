```python
# reproducer.py
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.template import Template, Context
from django.urls import path

# Minimal Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='asecretkey',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [],
            },
        },
    ],
)


def index(request):
    template = Template('{{ list_var|random }}')
    context = Context({"list_var": []})
    return HttpResponse(template.render(context))


urlpatterns = [
    path('', index),
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

if __name__ == '__main__':
    import sys
    from django.core.management.commands.runserver import Command as runserver
    from django.core.wsgi import get_wsgi_application
    from django.test import Client
    
    try:
        # Setup Django
        execute_from_command_line(['manage.py', 'migrate'])  # Setup database if needed
        application = get_wsgi_application()
        
        # Create a test client to simulate a request to the server
        client = Client()
        response = client.get('/')
        assert response.status_code == 200, "Expected an HTTP 200 response"
        
        print("No issue found: The server responded with an HTTP 200 status code.")
        sys.exit(0)
        
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script sets up a minimal Django application to test if the use of the `random` filter with an empty list causes an internal server error (status code 500). If the issue is present, it will raise an `AssertionError` or print a detailed stack trace of the raised exception. The script exits with code `0` when the issue is fixed.