import os
import subprocess

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
    # Set umask to 077
    os.umask(0o77)

    # Create a new project directory
    project_dir = "mysite"
    os.mkdir(project_dir)

    # Try to start a new Django project
    try:
        subprocess.run(["django-admin.py", "startproject", project_dir], check=True)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present: startproject does not honor umask")

    # Check the permissions of the settings file
    settings_file = os.path.join(project_dir, "settings.py")
    st = os.stat(settings_file)
    perms = oct(st.st_mode & 0o777)
    assert perms != "0o644", f"Issue is present: startproject does not honor umask (perms={perms})"

if __name__ == "__main__":
    main()
