import subprocess
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

def run_command(*args, **kwargs):
    try:
        return subprocess.run(*args, **kwargs, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("Command failed:", e.cmd, file=sys.stderr)
        print("Return code:", e.returncode, file=sys.stderr)
        print("Output:", e.output, file=sys.stderr)
        print("Error:", e.stderr, file=sys.stderr)
        raise

def main():
    project_dir = "phpmyadmin"

    try:
        # Ensure the project directory is not already present
        if os.path.exists(project_dir):
            raise AssertionError(f"The directory '{project_dir}' already exists. Please delete it and try again.")

        # Clone the phpMyAdmin repository
        run_command(['git', 'clone', '--depth', '1', 'https://github.com/phpmyadmin/phpmyadmin.git'])

        # Install Sphinx
        run_command(['pip', 'install', 'Sphinx==3.0.0'])  # Explicit version to match the issue's environment

        # Attempt to build the HTML documentation
        result = run_command(['make', 'html'], cwd=f"./{project_dir}/doc")

        # Check for the specific warning in stderr
        if "duplicate term description of mysql, other instance in glossary" not in result.stderr:
            raise AssertionError("Expected duplicate term warning not found")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Issue reproduced successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
