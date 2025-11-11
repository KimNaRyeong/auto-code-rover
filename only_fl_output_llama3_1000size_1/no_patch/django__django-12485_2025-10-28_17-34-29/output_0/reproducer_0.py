import requests
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.base import ContentFile
import unittest
from io import BytesIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    url = 'http://localhost:8000/upload/'
    data = {
        "file": ("测试.txt", BytesIO(b"test"), 'text/plain')
    }
    response = requests.post(url, files=data)
    if response.status_code != 200:
        raise AssertionError("Failed to upload file")
    try:
        handler = FileUploadHandler(BytesIO(response.content))
        content_file = ContentFile(handler.get_file_name())
        assert content_file.name == "测试.txt", f"Expected '测试.txt' but got {content_file.name}"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
