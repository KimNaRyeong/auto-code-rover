import os
import stat
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

    # Create a new directory for the project
    project_dir = "mysite"
    os.mkdir(project_dir)

    # Try to start a new Django project with django-admin.py
    try:
        subprocess.check_call(["django-admin.py", "startproject", "mysite"], cwd=project_dir)
    except IOError as e:
        print_stacktrace(e)
        assert False, "Failed to create project due to permission denied"

    # Check the permissions of settings.py
    settings_file = os.path.join(project_dir, "mysite", "settings.py")
    st = os.stat(settings_file)
    mode = st.st_mode & 0o777
    assert mode != 0o644, f"Expected mode to be not 0644, but got {mode:o}"

if __name__ == "__main__":
    main()
