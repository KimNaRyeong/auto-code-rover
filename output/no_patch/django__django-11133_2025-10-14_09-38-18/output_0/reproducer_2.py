import sys
import django
from django.conf import settings
from django.http import HttpResponse
import traceback

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

def main():
    try:
        # Configure Django settings
        settings.configure(
            DEBUG=True,
            SECRET_KEY='testsecret',
            ROOT_URLCONF=__name__,
            MIDDLEWARE=[],
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            }
        )
        django.setup()
        
        # Scenario 1: String content.
        response = HttpResponse("My Content")
        assert response.content == b"My Content", "Failed: String content does not match expected value."

        # Scenario 2: Bytes content.
        response = HttpResponse(b"My Content")
        assert response.content == b"My Content", "Failed: Bytes content does not match expected value."

        # Scenario 3: Memoryview content.
        response = HttpResponse(memoryview(b"My Content"))
        assert response.content == b"My Content", "Failed: Memoryview content does not match expected value."

        print("All tests passed. Issue is fixed.")
        sys.exit(0)

    except AssertionError as ae:
        print_stacktrace(ae)
        raise ae  # Re-raise the AssertionError to show the detailed stack trace in the terminal.

if __name__ == "__main__":
    main()
