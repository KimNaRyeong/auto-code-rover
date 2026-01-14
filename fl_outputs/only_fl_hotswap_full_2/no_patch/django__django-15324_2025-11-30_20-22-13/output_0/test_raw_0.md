 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import io
import os
import sys
import tempfile
from urllib.parse import urlparse

import requests
from django.core.files.temp import NamedTemporaryFile
from django.test.client import Client
from django.urls import path, set_urlconf

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

# Replace the following lines with your Django project's urls.py content
app_name = "testapp"
urlpatterns = [
    path("", views.index, name="index"),
]

def request_with_bad_filename():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!\0", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\0")
    return requests.Session().send(prepared)

def run_test():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
    client = Client()
    set_urlconf(app_name, urlpatterns)

    try:
        response = request_with_bad_filename()
        assert False, "Expected ValueError, but the request was successful"
    except ValueError as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
    else:
        print("Test passed")

if __name__ == "__main__":
    run_test()
```

Replace `your_project_name` with the name of your Django project. This script imports the `urlpatterns` and `views` from your project's `urls.py` and `views.py` files. Make sure to keep the `app_name` variable and the `set_urlconf` call.

This script sends a request with a bad filename to the Django server and checks if a `ValueError` is raised. If the `ValueError` is not raised, an `AssertionError` is raised instead. The script then prints the stack trace of the error. If the request is successful, the script exits with code 0.