```python
import subprocess
import os
import shutil

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

def setup_sphinx_project():
    # Creating a fresh Sphinx project using sphinx-quickstart
    subprocess.run(["sphinx-quickstart", "--project", "proj", "--sep", "--author", "me", "--release", "1.0", "--language", "en", "-q", "."], check=True)
    with open("source/index.rst", "a") as f:
        f.write("\n`foo <https://google.com/test.txt#test>`_")

def run_linkcheck():
    # Running the linkcheck and capturing the output
    result = subprocess.run(["make", "linkcheck"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout + result.stderr

def main():
    setup_sphinx_project()
    try:
        output = run_linkcheck()
        error_message = "404 Client Error: Not Found for url: https://google.com/test.txt"
        # Verifying if the expected failure message is present in linkcheck's output
        assert error_message in output, "Linkcheck did not report the HTTP error."
    except AssertionError as e:
        print_stacktrace(e)
        # Cleanup before exit
        cleanup()
        exit(1)
    except Exception as e:
        print("Unexpected error during the replication process.")
        print_stacktrace(e)
        # Cleanup before exit
        cleanup()
        exit(1)
    else:
        print("Issue is fixed.")
        # Cleanup before success exit
        cleanup()
        exit(0)

def cleanup():
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("source"):
        shutil.rmtree("source")
    for file in ["Makefile", "make.bat"]:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by:

1. Automatically generating a Sphinx project with `sphinx-quickstart`.
2. Appending a broken link with an anchor to the `index.rst` file.
3. Running the `linkcheck` build command using `make`.
4. Checking the output from `linkcheck` for the specific 404 error message.
5. If the error message indicates "Anchor 'test' not found" when the server responded with a 404 or another HTTP error code, the script raises an `AssertionError`.
6. It uses a `try` block to catch the AssertionError and print a stack trace specifically for this error. It also catches any other `Exception`, prints a debug stack trace, and then performs a cleanup.
7. On successful completion without errors (indicating that the issue is presumably fixed), it prints "Issue is fixed.".
8. Regardless of the outcome, it attempts to cleanup the generated and modified files to maintain a clean state.