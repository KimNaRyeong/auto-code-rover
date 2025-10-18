import os
import sys
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

def test_startproject_honors_umask():
    # Setting the umask to 0o077 so that all newly created files 
    # should have at most 'rwx------' permissions
    original_umask = os.umask(0o077)

    try:
        project_name = "test_project"
        # Use Django's internal mechanism to create files, simulating the startproject command
        # Since using Django internals requires Django set up, ensure Django is available:
        from django.core.management import call_command
        call_command("startproject", project_name)

        # The settings.py file is a good test case for checking permissions
        settings_path = os.path.join(project_name, "settings.py")
        if not os.path.exists(settings_path):
            raise AssertionError("Failed to create settings.py, startproject might not have worked as expected.")

        # Check permissions of the file, expecting them to respect the umask
        stat_result = os.stat(settings_path)
        file_permissions = oct(stat_result.st_mode)[-3:]
        
        # Expect permissions to be '-rw-------' or similar, since umask is 0o077
        # This checks for '600' permission, as Python's os module deals with permissions in octal format
        if file_permissions != '600':
            raise AssertionError(f"settings.py permissions do not honor umask 077. Permissions are: {file_permissions}")

        print("Test passed: startproject honors umask.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        os.umask(original_umask)  # Restore original umask
        if os.path.exists(project_name):
            # Clean up - remove the created project directory after checking
            import shutil
            shutil.rmtree(project_name)
    
if __name__ == "__main__":
    test_startproject_honors_umask()
