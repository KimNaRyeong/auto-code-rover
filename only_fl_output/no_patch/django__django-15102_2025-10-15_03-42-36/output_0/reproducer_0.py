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
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def set_umask_and_create_file():
    original_umask = os.umask(0o077)
    try:
        # Attempt to create a project directory simulating django-admin startproject
        project_name = "testproject"
        subprocess.run(["python3", "-m", "django", "startproject", project_name], check=True)
        
        # Check file permissions of a known file, e.g., settings.py
        settings_file = os.path.join(project_name, project_name, "settings.py")
        if os.path.exists(settings_file):
            file_stat = os.stat(settings_file)
            # Resetting umask to original after checking
            os.umask(original_umask)
            # Checking if the file respects the umask setting
            if oct(file_stat.st_mode)[-3:] != '600':
                raise AssertionError(f"File permissions do not honor umask: {oct(file_stat.st_mode)}")
            else:
                print("The issue is fixed. Exiting with code 0.")
                sys.exit(0)
        else:
            raise FileNotFoundError("settings.py not found")
    except Exception as e:
        os.umask(original_umask)  # Reset umask to original in case of exception
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    set_umask_and_create_file()
