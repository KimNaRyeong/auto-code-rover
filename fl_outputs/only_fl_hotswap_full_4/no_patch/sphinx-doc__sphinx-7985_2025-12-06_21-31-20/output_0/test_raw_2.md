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

def main():
    # Create a template project with sphinx-quickstart
    subprocess.run(["sphinx-quickstart", "template_project"], check=True)

    # Write the following to index.rst in the template project
    index_rst = """\
broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
"""
    with open("template_project/source/index.rst", "w") as f:
        f.write(index_rst)

    # Run `make linkcheck` in the template project
    result = subprocess.run(["make", "-C", "template_project", "linkcheck"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             check=True)

    # Check for the local link check
    if b"looking for now-outdated files... none found" not in result.stderr:
        raise AssertionError("Local link check not performed")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, create a new directory and save the code block above as `reproducer.py` in that directory. Then, run the script with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.