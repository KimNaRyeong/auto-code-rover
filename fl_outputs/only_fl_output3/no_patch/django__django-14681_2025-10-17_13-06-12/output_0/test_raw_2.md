Given the constraints and the aim to create a standalone Python script (`reproducer.py`) that reproduces the issue and follows your error handling and output format requirements, I'll provide a script template applicable to a Django project setup. This script assumes a Django project setup similar to the description and will attempt to simulate the file upload scenarios to reproduce the CSRF error under different storage configurations.

Please note, this script needs to be adjusted according to the actual project's structure, specifically the `DJANGO_SETTINGS_MODULE` path, which should match your Django project's settings module path.

```python
import os
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csrfbug.settings')
import django
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.management import call_command
from django.conf import settings

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

# Function to simulate file upload
def simulate_file_upload(client, filename='test_file.txt', content=b'Test file content', content_type='text/plain'):
    file = SimpleUploadedFile(filename, content, content_type=content_type)
    response = client.post('/admin/app/file/add/', {'file': file}, follow=True)
    return response

# Setup function to prepare environment
def setup_environment():
    call_command('migrate')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'password')

try:
    # Setup environment: Ensure database and superuser are prepared
    setup_environment()

    # Initialize testing client
    client = Client()

    # Log in as the superuser
    assert client.login(username='admin', password='password'), "Superuser login failed."

    # Scenario 1: Ensure default state works
    response = simulate_file_upload(client)
    assert response.status_code != 403, "Unexpected CSRF error in default state."

    # Scenario 2: Remove media/tmp directory and try to upload
    tmp_dir_path = os.path.join(settings.MEDIA_ROOT, 'tmp')
    if os.path.exists(tmp_dir_path):
        os.rmdir(tmp_dir_path)
    
    try:
        response = simulate_file_upload(client)
        assert response.status_code == 403, "Expected a CSRF error due to missing temp directory."
    finally:
        # Cleanup - recreate the tmp directory
        os.mkdir(tmp_dir_path)

    # Scenario 3: Remove whole media directory and try to upload
    if os.path.exists(settings.MEDIA_ROOT):
        os.rmdir(settings.MEDIA_ROOT)
    
    try:
        response = simulate_file_upload(client)
        assert response.status_code == 403, "Expected a CSRF error due to missing MEDIA_ROOT directory."
    finally:
        # Cleanup - recreate the media directory
        os.mkdir(settings.MEDIA_ROOT)

    print("The issue was not reproduced. Exiting with code 0.")
    sys.exit(0)

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script automates the process of reproducing the CSRF failure issue you've described under various file storage configurations. Ensure that the paths and the setup configurations like the Django settings module match your project setup. Also, replace `'password'` with the actual superuser password used in your setup.

This script should be placed in the root directory of your Django project and executed with Python 3. Ensure you've provided the necessary permissions and setup for the script to modify directories and access the Django environment correctly.