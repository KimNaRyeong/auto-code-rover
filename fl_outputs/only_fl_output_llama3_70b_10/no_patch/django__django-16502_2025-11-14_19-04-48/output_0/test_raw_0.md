Here is the `reproducer.py` file to reproduce the issue:
```
import os
import subprocess
from urllib.parse import urlparse

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

def run_server():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test.settings'
    import django
    django.setup()
    from django.core.management.commands.runserver import run_server
    run_server()

def main():
    try:
        # Create a new Django project
        subprocess.check_call(['django-admin', 'startproject', 'django_test'])
        os.chdir('django_test')

        # Start the development server
        server_process = subprocess.Popen(['python3', 'manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the server to start
        while True:
            line = server_process.stdout.readline().decode('utf-8').strip()
            if 'Starting development server' in line:
                break

        # Send a HEAD request to the server
        url = urlparse('http://127.0.0.1:8000/')
        response = subprocess.check_output(['curl', '-iX', 'HEAD', f'http://{url.netloc}{url.path}'])

        # Check if the response body is empty
        assert b'</html>' not in response, "Response body is not empty"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
```
This script creates a new Django project, starts the development server, sends a HEAD request to the server using `curl`, and checks if the response body is empty. If the response body is not empty, it raises an `AssertionError` with a stack trace.

To run this script, save it as `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.