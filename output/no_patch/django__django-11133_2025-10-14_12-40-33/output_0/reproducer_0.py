# reproducer.py
from django.http import HttpResponse
from django.conf import settings
import os

# Function to print stack trace
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

# Minimal Django setup
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    ROOT_URLCONF=__name__,
)

def main():
    # Testing various types of response content
    try:
        # String content
        response = HttpResponse("My Content")
        string_content = response.content
        assert string_content == b'My Content', "Mismatch in string content"

        # Bytes content
        response = HttpResponse(b"My Content")
        bytes_content = response.content
        assert bytes_content == b'My Content', "Mismatch in bytes content"

        # memoryview content
        response = HttpResponse(memoryview(b"My Content"))
        memoryview_content = response.content
        assert memoryview_content == b'My Content', f"Expected b'My Content', got {memoryview_content}"

        print("All tests passed!")

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    import django
    django.setup()
    main()
