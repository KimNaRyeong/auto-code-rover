To fulfill your request, I'll create a script that attempts to reproduce the described issue with handling HEAD requests improperly by a Django development server. This assignment entails setting up a minimal Django project programmatically, running a development server, making a HEAD request to the server, and verifying whether the response contains a body, which should not happen according to the specifications. If the issue is present (i.e., the response body is not empty for a HEAD request), the script will raise an `AssertionError`. If Django has fixed the issue and the test passes (i.e., the response body is empty for a HEAD request), the script will exit with code 0 without error.

```python
import subprocess
import threading
import time
import requests
import sys
import os

# Utility function to print the stack trace cleanly.
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

# Function to programmatically create a minimal Django project.
def create_django_project():
    try:
        # Generate a new Django project with a random, unique name to avoid conflicts.
        project_name = "test_project_{}".format(int(time.time()))
        os.system(f'django-admin startproject {project_name}')
        return project_name
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

# Function to serve the Django project using Django's development server.
def serve_django_project(project_name):
    def runserver():
        os.chdir(project_name)
        subprocess.run(['python', 'manage.py', 'runserver'])

    server_thread = threading.Thread(target=runserver)
    server_thread.daemon = True
    server_thread.start()

# Function to make a HEAD request and verify the result.
def verify_issue():
    try:
        time.sleep(3)  # Give the server some time to start
        response = requests.head('http://127.0.0.1:8000/')
        assert response.content == b'', "HEAD request should not return a body."
        print("Success: The issue is not present.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    project_name = create_django_project()
    serve_django_project(project_name)
    verify_issue()
    sys.exit(0)
```

This standalone Python script `reproducer.py`, when placed in a Django environment and executed, should adequately attempt to reproduce the described issue. It dynamically creates a new Django project to avoid interfering with existing projects, starts the Django development server in a separate thread, and then makes a HEAD request to verify whether the issue is present based on the response body being non-empty. It employs the function provided for printing stack traces to ensure that any exceptions raised are clearly reported.