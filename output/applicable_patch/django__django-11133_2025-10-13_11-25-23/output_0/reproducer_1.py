import sys
from django.conf import settings
from django.http import HttpResponse

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

def configure_django_settings():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='a_random_secret_key',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*']
    )

def test_memoryview_in_httpresponse():
    try:
        # Configure Django settings
        configure_django_settings()
        
        # memoryview content
        response = HttpResponse(memoryview(b"My Content"))
        expected_content = b"My Content"
        actual_content = response.content

        # Raise an assertion error if the actual content does not match the expected content.
        assert actual_content == expected_content, (
            f"Expected content {expected_content}, but got {actual_content}."
        )
        
    except Exception as e:
        print_stacktrace(e)
        raise  # re-raise the exception to indicate the test failure

if __name__ == "__main__":
    try:
        test_memoryview_in_httpresponse()
        print("Test passed. HttpResponse handles memoryview objects correctly.")
        sys.exit(0)  # Exit with code 0 when the issue is fixed
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate that the issue is present
