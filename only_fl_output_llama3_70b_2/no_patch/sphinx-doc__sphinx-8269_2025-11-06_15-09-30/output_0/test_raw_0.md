Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import subprocess

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
    # Create a new Sphinx project
    subprocess.run(["sphinx-quickstart", "--project", "proj", "--sep", "--author", "me", "--release", "1.0", "--language", "en"])

    # Create an RST file with a link to a non-existent URL
    with open("source/index.rst", "a") as f:
        f.write("\n`foo <https://google.com/test.txt#test>`_")

    # Run linkcheck with linkcheck_anchors=True
    os.environ["LINKCHECK_ANCHORS"] = "True"
    result = subprocess.run(["make", "linkcheck"], capture_output=True, text=True)

    # Check if the output reports an anchor not found error instead of HTTP error
    if "Anchor 'test' not found" in result.stdout:
        raise AssertionError("Linkcheck reports anchor not found error instead of HTTP error")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a new Sphinx project, adds an RST file with a link to a non-existent URL, runs `make linkcheck` with `linkcheck_anchors=True`, and checks if the output reports an anchor not found error instead of HTTP error. If it does, it raises an `AssertionError` with a stack trace.