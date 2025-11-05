Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import io
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
settings.configure(DEBUG=True, ALLOWED_HOSTS=['*'])

def print_stacktrace(e: Exception):
    import traceback    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(repr(request.FILES['docfile']))
            return HttpResponse('OK')
        else:
            print("Not valid!")
            return HttpResponse('Not valid!')
    else:
        form = UploadFileForm()
        return render(request, 'uploads/index.html', {'form': form})

class UploadFileForm(forms.Form):
    docfile = forms.FileField()

def reproduce_issue():
    try:
        contents = io.StringIO("." * (1024 * 1024 * 3))
        files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
        req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
        prepared = req.prepare()
        body = prepared.body
        assert isinstance(body, bytes)
        prepared.body = body.replace(b"!", b"\x00")
        session = requests.Session()
        response = session.send(prepared)
        if response.status_code == 500:
            raise AssertionError("Issue is present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    from django.core.management import run_from_argv
    argv = ['reproducer.py', 'runserver']
    run_from_argv(argv)
    reproduce_issue()
```
This script sets up a Django development server, defines an `index` view to handle file uploads, and sends a request with a file containing a null byte in its filename. It then checks if the response status code is 500. If it is, it raises an `AssertionError` with a stack trace of the issue. If any other exception occurs during the execution, it also prints the stack trace and exits with code 1.

Please note that you need to create a directory named `uploads` in the same directory as this script, and inside it, create a file named `index.html` for the view to render.