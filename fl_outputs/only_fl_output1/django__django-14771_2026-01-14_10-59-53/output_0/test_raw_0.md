```python
import os
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, ": ", code_context, file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_auto_reloader_passes_xoptions():
    """
    Test whether Django's runserver command correctly passes -X options to the auto reloader
    when the Django development server is started with specific -X options.
    """
    # Prepare a simulation environment
    project_name = "my_test_project"
    app_name = "my_test_app"
    
    # Ensure the current script is run from the project's root directory
    cwd = os.getcwd()
    
    # Simulate creating a Django project and app
    subprocess.run(["django-admin", "startproject", project_name], check=True)
    os.chdir(os.path.join(cwd, project_name))
    subprocess.run(["python", "-m", "django", "startapp", app_name], check=True)
    
    # Add a custom AppConfig to test the auto-reloader behavior
    apps_py_content = """
from django.apps import AppConfig
import sys

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_test_app'

    def ready(self):
        encoding = sys.getfilesystemencoding()
        print(f"=== {encoding}")
        with open("check_encoding.txt", "w") as f:
            f.write(encoding)
"""

    with open(os.path.join(app_name, "apps.py"), "w") as f:
        f.write(apps_py_content)
    
    # Modify the project settings to include the new app
    settings_path = os.path.join("my_test_project", "settings.py")
    with open(settings_path, "r") as f:
        settings_content = f.read()
    settings_content += f"\nINSTALLED_APPS += ['{app_name}']\n"
    with open(settings_path, "w") as f:
        f.write(settings_content)

    # Test running the server with -X utf8 option and check the file content
    try:
        subprocess.run(["python", "-X", "utf8", "manage.py", "runserver", "8005", "--noreload"], check=True, timeout=10)
    except subprocess.TimeoutExpired:
        pass  # Expected to manually interrupt the server after a short wait

    # Verify the output
    with open("check_encoding.txt", "r") as f:
        encoding = f.read().strip()
    
    os.chdir(cwd)  # Change back to the original directory
    
    # Assertion to check whether the desired encoding is set
    assert encoding == "utf-8", "The auto-reloader did not pass -X utf8 option to the subprocess."
    

try:
    test_auto_reloader_passes_xoptions()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("No issue detected.")
sys.exit(0)
```

This script attempts to reproduce the issue by creating a Django project and app within a temporary environment, modifies the `apps.py` of the app to check the file system encoding (which should be affected by the `-X utf8` option if passed correctly), and then runs the development server with this option. It checks if the encoding is set to UTF-8 as expected to verify the issue. If the encoding is not UTF-8, it raises an `AssertionError`, indicating the problem is present.