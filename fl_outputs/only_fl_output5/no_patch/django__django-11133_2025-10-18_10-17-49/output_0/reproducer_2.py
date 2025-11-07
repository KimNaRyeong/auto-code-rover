import os
import sys
from django.http import HttpResponse

def setup_django_environment():
    # Setup minimal Django settings required for testing
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer_settings')
    settings_module = """
SECRET_KEY = 'fake-key-for-testing-purposes-only'
INSTALLED_APPS = []
"""
    with open('reproducer_settings.py', 'w') as f:
        f.write(settings_module)
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['django-admin', 'check'])

    # Cleanup by removing the temporary settings module after use
    os.remove('reproducer_settings.py')

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

def main():
    try:
        # Ensure Django environment is correctly set up
        setup_django_environment()
        
        # Test HttpResponse with memoryview
        response = HttpResponse(memoryview(b"My Content"))
        assert response.content == b"My Content", "HttpResponse did not correctly handle memoryview object"

        # If the assertion passes, exit with code 0 signaling issue is fixed or not present
        print("Issue not present, successfully handled memoryview object.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        # If an error occurs, indicate failure to handle memoryview objects correctly
        sys.exit(1)

if __name__ == "__main__":
    main()
