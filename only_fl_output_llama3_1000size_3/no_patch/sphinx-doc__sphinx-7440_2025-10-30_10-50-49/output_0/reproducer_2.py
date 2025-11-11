import os
import sphinx
from sphinx.util import logging
import subprocess
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        # Clone the PHPMyAdmin repository
        if not os.path.exists("phpmyadmin"):
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/phpmyadmin/phpmyadmin.git"])
        os.chdir("phpmyadmin/doc")

        # Install Sphinx
        subprocess.run(["pip", "install", "'Sphinx'"])

        # Build the documentation
        subprocess.run(["make", "html"])

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to reproduce the issue")

if __name__ == "__main__":
    main()
