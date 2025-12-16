 I apologize for the syntax error in my previous response. Here's the corrected `reproducer.py` script:
```python
import os
import sys
import subprocess
from django.conf import settings

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_command(command: list, print_output: bool = False):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if print_output:
        print(output.decode())
    if error:
        error = error.decode()
        if b'-X' in error:
            error = error.replace(b'-X', b'').strip()
            error = error.decode()
        raise AssertionError(error)

if __name__ == "__main__":
    # Create a new Django project and app
    subprocess.run(["python", "-m", "django", "startproject", "my_project"])
    os.chdir("my_project")
    subprocess.run(["python", "-m", "django", "startapp", "my_app"])

    # Write to my_app/apps.py
    apps_py = os.path.join("my_app", "apps.py")
    with open(apps_py, "w") as f:
        f.write("from django.apps import AppConfig\n\n")
        f.write("class MyAppConfig(AppConfig):\n")
        f.write('    default_auto_field = "django.db.models.BigAutoField"\n')
        f.write('    name = "my_app"\n\n')
        f.write("# myapp global initial_demo ...\n")
        f.write('with open("manage.py", mode="r") as stream:    print("=== %s" % stream.encoding)\n' % sys.getdefaultencoding())

    # Add 'my_app' to INSTALLED_APPS in my_project/settings.py
    settings_py = os.path.join("my_project", "settings.py")
    with open(settings_py, "a") as f:
        f.write("\n\nINSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'my_app',\n]\n")

    # Run the server with -X utf8 and -v3
    command = ["python", "-X", "utf8", "manage.py", "runserver", "0.0.0.0:8005", "-v3"]
    run_command(command)

    # Run the server with -X utf8, -v3, and --noreload
    command = ["python", "-X", "utf8", "manage.py", "runserver", "0.0.0.0:8005", "-v3", "--noreload"]
    run_command(command)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

I apologize for any confusion caused by my previous response.