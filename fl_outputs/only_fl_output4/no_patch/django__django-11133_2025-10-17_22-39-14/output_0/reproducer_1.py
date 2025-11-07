# reproducer.py
import os
import django
from django.conf import settings

# Minimal required settings for Django
MINIMAL_DJANGO_SETTINGS = {
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'SECRET_KEY': 'fake-key',
}


def setup_django_environment():
    """Sets up Django environment with minimal settings necessary for testing."""
    settings.configure(**MINIMAL_DJANGO_SETTINGS)
    django.setup()


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


def test_memoryview_handling():
    from django.http import HttpResponse

    try:
        # Test with string content
        response = HttpResponse("My Content")
        assert response.content == b"My Content", "String content mismatch"
        
        # Test with bytes content
        response = HttpResponse(b"My Content")
        assert response.content == b"My Content", "Bytes content mismatch"
        
        # Test with memoryview content
        response = HttpResponse(memoryview(b"My Content"))
        # This assertion checks if the issue is present
        assert response.content == b"My Content", "Memoryview content mishandled"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("All tests passed")
        exit(0)


if __name__ == "__main__":
    setup_django_environment()
    test_memoryview_handling()
