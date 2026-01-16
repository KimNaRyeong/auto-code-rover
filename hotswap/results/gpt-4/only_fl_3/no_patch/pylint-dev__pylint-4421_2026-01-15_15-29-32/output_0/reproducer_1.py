# reproducerer.py
import subprocess
import sys
import os

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

def setup_environment():
    """Set up a Python virtual environment and install necessary packages."""
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    subprocess.check_call([os.path.join("venv", "bin", "python"), "-m", "pip", "install", "pylint==2.8.2", "pylint-quotes==0.2.1"])

def create_test_files():
    with open("pylintrc", "w") as file:
        file.write("""
[MASTER]
load-plugins=pylint_quotes
        """)
    with open("demo.py", "w") as file:
        file.write('foo = "bar"')

def run_pylint_and_check_error():
    result = subprocess.run([os.path.join("venv", "bin", "pylint"), "--rcfile", "pylintrc", "demo.py"], capture_output=True, text=True)
    if result.returncode != 0 and "TypeError: '<' not supported between instances of 'int' and 'str'" in result.stderr:
        raise AssertionError("PyLint plugin 'pylint-quotes' failed due to version comparison issue.")
    elif result.returncode == 0:
        print("No issue detected with pylint-quotes.")

def main():
    try:
        setup_environment()
        create_test_files()
        run_pylint_and_check_error()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
