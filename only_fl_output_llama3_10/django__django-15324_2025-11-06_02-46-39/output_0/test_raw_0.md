Here is the reproducer script:

```python
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(repr(request.FILES['docfile']))
            return HttpResponse('OK')
        else:
            print("Not valid!")
            return HttpResponse('NOT OK')
    else:
        form = UploadFileForm()
        return render(request, 'uploads/index.html', {'form': form})

def main():
    try:
        req = requests.Request("POST", "http://localhost:8000/", files={"docfile": (b"bogus.txt\x00!", io.BytesIO(b"." * 1024 * 1024 * 3), "text/plain")}, data={})
        prepared = req.prepare()
        body = prepared.body
        assert isinstance(body, bytes)
        prepared.body = body.replace(b"!", b"\x00")
        requests.Session().send(prepared)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sends a POST request to the Django view with a file name that contains null characters. If the issue is present, it will raise an `AssertionError` and print the stack trace using the provided function.