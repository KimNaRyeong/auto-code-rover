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
    import sys
    import subprocess

    # Install specific versions of pylint, astroid, and pylint-quotes
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pylint==2.8.2", "astroid==2.5.6", "pylint-quotes==0.2.1"])

    demo_code = """
foo = "bar"
"""
    pylintrc = """
[MASTER]
load-plugins=pylint_quotes
[STRING_QUOTES]
string-quote=single
docstring-quote=single
"""

    with open('demo.py', 'w') as file:
        file.write(demo_code)

    with open('pylintrc', 'w') as file:
        file.write(pylintrc)

    try:
        # Attempt to lint the demo.py file using pylint with the custom pylintrc
        output = subprocess.check_output([sys.executable, "-m", "pylint", "--rcfile", "pylintrc", "demo.py"], stderr=subprocess.STDOUT)
        print("No issue detected.")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1) # Exits with a non-zero code indicating failure due to an unexpected exception

    # If script reaches this point, issue was not encountered
    sys.exit(0) # Exit indicating the issue does not exist

if __name__ == "__main__":
    main()
