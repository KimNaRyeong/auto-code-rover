import os
import sys
import tempfile
from django.core.management import execute_from_command_line
import stat

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

def reproduce_issue():
    temp_dir = tempfile.mkdtemp()
    project_name = 'mysite'
    original_umask = os.umask(0o077)  # Set umask to 0o077
    try:
        sys.argv = ['manage.py', 'startproject', project_name, temp_dir]
        execute_from_command_line(sys.argv)  # Using Django's functionality

        settings_file_path = os.path.join(temp_dir, project_name, 'settings.py')
        if not os.path.isfile(settings_file_path):
            raise AssertionError("settings.py was not created.")
        
        # Check file permissions against expected permissions
        st = os.stat(settings_file_path)
        actual_permissions = stat.S_IMODE(st.st_mode)
        expected_permissions = 0o600  # Expected due to umask setting of 0o077

        if actual_permissions != expected_permissions:
            error_msg = f"Permissions of settings.py do not match expected permissions. " \
                        f"Expected: {oct(expected_permissions)}, Got: {oct(actual_permissions)}"
            raise AssertionError(error_msg)

    except Exception as e:
        print_stacktrace(e)
        os.umask(original_umask)  # Restore original umask
        sys.exit(-1)
    
    os.umask(original_umask)  # Restore original umask
    print("Issue not present, or the test did not reproduce the issue.")
    sys.exit(0)

if __name__ == "__main__":
    if 'django' not in sys.modules:
        print("Django is required to run this script. Please install it and try again.")
        sys.exit(-1)
    reproduce_issue()
