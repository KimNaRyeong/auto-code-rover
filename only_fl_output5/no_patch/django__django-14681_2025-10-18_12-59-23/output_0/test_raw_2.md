Given the parameters and constraints, I'll draft an illustrative standalone python file named `reproducer.py` that simulates the network requests to a running Django development server in order to reproduce the issue described. This script will specifically aim to demonstrate the CSRF failure during file uploads when there is a problem with the server's storage setup (like missing directories). However, to fully execute it as intended, ensure that the Django project is configured and running per the described settings and that you've already completed the required setup including migrations and superuser creation.

```python
import requests
from pathlib import Path

# Function to print stack trace for exceptions
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

# Details for login
login_url = "http://127.0.0.1:8000/admin/login/"
admin_page = "http://127.0.0.1:8000/admin/app/file/add/"
username = 'admin'  # Change as necessary
password = 'password'  # Change as necessary

# Start a session to keep cookies
s = requests.Session()

# Retrieve CSRF token
r1 = s.get(login_url)
csrftoken = r1.cookies['csrftoken']

# Perform login
login_data = {'username': username, 'password': password, 'csrfmiddlewaretoken': csrftoken, 'next': '/admin/'}
r2 = s.post(login_url, data=login_data, headers=dict(Referer=login_url))

# Ensure login was successful
assert "Welcome" in r2.text, "Login failed, please check your username and password"

# Attempt to upload a file
files = {'file': ('test.txt', 'This is a test file')}
data = {'csrfmiddlewaretoken': csrftoken}

try:
    upload_response = s.post(admin_page, files=files, data=data, headers={'Referer': admin_page})
    
    # Check for expected error message
    if not upload_response.ok or "error" in upload_response.text.lower():
        print("File upload failed as expected due to a storage issue.")
    else:
        raise AssertionError("File upload succeeded unexpectedly.")

except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Script completed successfully.")
exit(0)
```

This script assumes a running Django development server configured as per your description. It tries to simulate the file upload process to the '/admin/app/file/add/' URL, including handling CSRF tokens for authentication purposes.

Please adjust the `username` and `password` variables to match your superuser credentials. This script does not directly interact with Django internals or the filesystem, so you need to manually ensure the media directory and its subdirectories are set up correctly per the scenarios described for testing.

Run this script after starting your Django project with `python manage.py runserver`. Remember, this is an approximation and may require adjustments based on the actual configuration of your project and how it handles uploads and authentication.