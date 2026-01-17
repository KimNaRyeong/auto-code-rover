Below is a standalone Python script named `reproducer.py`, designed to automate the process of reproducing the issue related to the auto-reloading mechanism not tracking changes in `manage.py` as described. This script simulates the modification of the `manage.py` file and checks whether Django's auto-reloader detects this change. If the issue is present (i.e., changes in `manage.py` are not detected, and thus, the auto-reloader doesn't trigger), the script will print a stack trace and raise an `AssertionError`.

Remember, this script needs to be placed in the root directory of your Django project (next to `manage.py`) and requires Python 3.6.2 and Django 2.2.1 as per the described environment. Please adjust the script as needed for your environment, including the path to `manage.py` if required.

```python
import subprocess
import time
import os
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

def modify_manage_py():
    with open('manage.py', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("print('Modified for testing')\n" + content)

def check_reloader_triggered(original_stdout: str):
    # Wait a bit for the auto-reloader to pick up the changes.
    time.sleep(5)
    with open('django_server_output.txt', 'r') as f:
        output = f.read()
        return original_stdout != output

def main():
    try:
        # Ensure `manage.py` is in its original state.
        subprocess.run(['git', 'checkout', 'manage.py'], check=True)

        # Start Django development server in the background.
        server_process = subprocess.Popen(
            ['python3', 'manage.py', 'runserver'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        time.sleep(3)  # Wait a bit for the server to fully start.
        original_stdout = server_process.stdout.read()

        modify_manage_py()  # Trigger potential auto-reload.

        assert check_reloader_triggered(original_stdout), "Auto-reloader did not detect changes in manage.py"
        
        print("Success: Auto-reloader detected changes in manage.py")

    except AssertionError as e:
        print_stacktrace(e)
        raise e
    except Exception as e:
        print_stacktrace(e)
        raise e
    finally:
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("Server process terminated.")

if __name__ == "__main__":
    main()

```
Please note:
- This script assumes you are in a Git repository and uses `git checkout manage.py` to ensure `manage.py` returns to its original state before each run. This may not be suitable for all environments, especially where `manage.py` is not tracked by Git or modifications should be retained. Adjust as necessary.
- The `check_reloader_triggered` function might need adjustments based on the specifics of your project and environment, especially regarding how it checks if the auto-reloader was triggered.
- The delay used in `time.sleep()` calls is somewhat arbitrary to allow the server to start and to detect file changes. Depending on your system's performance, you might need to adjust these delays.