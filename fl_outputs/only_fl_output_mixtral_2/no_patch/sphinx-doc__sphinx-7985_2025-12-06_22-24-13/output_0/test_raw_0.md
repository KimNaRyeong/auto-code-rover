 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_linkcheck():
    try:
        subprocess.check_call(["make", "linkcheck"], cwd="template_project")
    except subprocess.CalledProcessError as e:
        return e

def main():
    template_project_dir = "template_project"
    try:
        # Create template project with sphinx-quickstart
        subprocess.check_call(["sphinx-quickstart", template_project_dir], cwd=".")

        # Modify index.rst in the template project
        with open(f"{template_project_dir}/source/index.rst", "a") as index_rst:
            index_rst.write("\nbroken local-link_\n\n.. _local-link: doesntexist\n")

        # Run linkcheck
        e = run_linkcheck()

        # Check for the expected error message
        expected_error_message = "broken    https://lkfqhlkghflkhs - HTTPSConnectionPool"
        if expected_error_message not in e.output.decode():
            raise AssertionError(f"Expected error message '{expected_error_message}' not found in output:\n{e.output.decode()}")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
To run the script, execute `python3 reproducer.py` in a terminal. The script will create a template project with `sphinx-quickstart`, modify the `index.rst` file to include a broken local link, and then run `make linkcheck`. If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.