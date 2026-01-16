import os
import sys
import subprocess
import tempfile
import venv

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


def install_dependencies(venv_path, packages):
    """Install packages using pip in the specified virtual environment."""
    pip_executable = os.path.join(venv_path, "bin", "pip")
    command = [pip_executable, "install"] + packages
    subprocess.run(command, check=True)


def run_pylint(venv_path, pylintrc_path, python_file):
    """Run pylint using the specified virtual environment."""
    pylint_executable = os.path.join(venv_path, "bin", "pylint")
    command = [pylint_executable, "--rcfile", pylintrc_path, python_file]
    result = subprocess.run(command, text=True, capture_output=True)
    return result


def main():
    # Define test code and rcfile content
    test_code = 'foo = "bar"'
    pylintrc_content = "[MASTER]\nload-plugins=pylint_quotes"
    packages = ["pylint==2.8.2", "pylint-quotes==0.2.1"]

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create and activate virtual environment
            venv_dir = os.path.join(temp_dir, "venv")
            venv.create(venv_dir, with_pip=True)

            # Install dependencies
            install_dependencies(venv_dir, packages)

            # Prepare test files
            py_file = os.path.join(temp_dir, "test.py")
            with open(py_file, "w") as pyfile:
                pyfile.write(test_code)

            pylintrc_file = os.path.join(temp_dir, "pylintrc")
            with open(pylintrc_file, "w") as rcfile:
                rcfile.write(pylintrc_content)

            # Run pylint with the test file
            result = run_pylint(venv_dir, pylintrc_file, py_file)

            # Analyze the results
            if "TypeError" in result.stderr:
                raise AssertionError("TypeError encountered while running pylint with pylint-quotes plugin")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error, indicating failure to run as expected or issue found

    print("No issues found. The problem might have been fixed.")
    sys.exit(0)  # Exit with success

if __name__ == "__main__":
    main()
