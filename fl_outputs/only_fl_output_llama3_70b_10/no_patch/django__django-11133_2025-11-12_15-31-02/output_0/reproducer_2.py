import sys
from django.http import HttpResponse
import django
from django.conf import settings

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

try:
    # Configure Django settings
    settings.configure(DEFAULT_CHARSET='utf-8')

    # Create a bytes object
    b = b"My Content"

    # Create a memoryview object from the bytes object
    mv = memoryview(b)

    # Create an HttpResponse with the memoryview object
    response = HttpResponse(mv)

    # Check if the content is correct
    assert response.content == b"My Content"

    print("Issue not present, exiting with code 0")
    sys.exit(0)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
