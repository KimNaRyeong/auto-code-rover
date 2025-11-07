import os
import sys
import stat
from django.core import management

def print_stacktrace(e: Exception):
    import traceback
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = traceback.extract_tb(e.__traceback__)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def set_umask_and_check_permissions():
    os.umask(0o077)
    project_name = "test_project"
    settings_path = os.path.join(project_name, project_name, "settings.py")
    
    try:
        # Using Django's command execution interface to simulate 'django-admin startproject'
        management.call_command('startproject', project_name)
        
        # Checking the permissions of the settings.py file
        file_stat = os.stat(settings_path)
        permissions = stat.S_IMODE(file_stat.st_mode)
        expected_permissions = 0o600  # Expected because umask is set to 077
        
        assert permissions == expected_permissions, f"settings.py permissions do not honor umask: {oct(permissions)}"

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    set_umask_and_check_permissions()
    print("Issue has been fixed or cannot be reproduced.")
    sys.exit(0)
