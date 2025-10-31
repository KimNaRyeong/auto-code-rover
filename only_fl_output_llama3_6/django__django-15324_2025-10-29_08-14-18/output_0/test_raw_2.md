Here is the reproducer script:

```python
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from wsgiref.simple_server import make_server

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

def reproduce_issue():
    settings.configure()
    form_data = {'docfile': (b'bad_file\x00.txt!', open('temp.txt', 'wb'), 'text/plain')}
    response = requests.post('http://localhost:8000/', files=form_data)
    if response.status_code == 500:
        print_stacktrace(response.exceptions[0])
        raise AssertionError("Issue reproduced")
    else:
        print("Issue not reproduced")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print(f"AssertionError: {e}")
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        form_data = {}
        for key in environ.get('wsgi.input').read().decode().split('&'):
            k, v = key.split('=')
            form_data[k] = v
        return HttpResponse(f"Form data: {form_data}")
    else:
        return HttpResponse("Invalid request method")

if __name__ == '__main__':
    httpd = make_server('localhost', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
```

This script sets up a simple WSGI server that listens for POST requests. When a request is received, it parses the form data and returns an HTTP response with the parsed data. The reproducer then sends a POST request to this server with the bad file name and checks if the server raises an exception. If an exception is raised, it prints the stack trace and raises an AssertionError.