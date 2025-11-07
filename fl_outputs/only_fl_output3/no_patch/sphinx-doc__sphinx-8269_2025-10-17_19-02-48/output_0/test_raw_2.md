To address your request for creating a stand-alone `reproducer.py` Python script to reproduce the described Sphinx `linkcheck` issue, where HTTP errors should be reported instead of an "Anchor not found" message, follow the below Python script. This script automates the creation of a minimal Sphinx project, modifies its configuration to enable `linkcheck_anchors`, injects a document with a broken link containing an anchor, and finally runs the Sphinx linkcheck to observe the reported error. The expectation is to catch an incorrect error message so that when the actual error matches the expected HTTP error instead of the anchor not found, the script does not raise an exception, indicating that the issue is fixed.

```python
import os
import subprocess
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

def create_sphinx_project():
    os.makedirs("source", exist_ok=True)
    with open("source/conf.py", "w") as f:
        f.write("""project = 'proj'
master_doc = 'index'
html_theme = 'alabaster'
linkcheck_anchors = True
""")
    with open("source/index.rst", "w") as f:
        f.write(""".. _start:

Welcome to proj's documentation!
=================================

References
----------

`foo <https://google.com/test.txt#test>`_
""")

def run_linkcheck():
    res = subprocess.run(["sphinx-build", "-b", "linkcheck", ".", "_build"], capture_output=True, text=True)
    return res

def verify_output(output):
    expected_error_fragment = "404 Client Error: Not Found for url"
    if expected_error_fragment not in output:
        raise AssertionError("Expected HTTP error not found in linkcheck output.")

def main():
    try:
        create_sphinx_project()
        result = run_linkcheck()
        verify_output(result.stdout + result.stderr)
        print("No issue detected, linkcheck reported HTTP errors as expected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with a non-zero code to indicate a failure to reproduce if needed

if __name__ == "__main__":
    main()
```

Before running this script, ensure you have Sphinx installed in your environment (`pip install sphinx`). Place this script at the root of your intended Sphinx project directory and execute it with `python3 reproducerer.py`. 

- If the issue is present, the script should raise an `AssertionError`, indicating that the expected HTTP error message was not found in the Sphinx `linkcheck` results, which means the script correctly identified the behavior where "anchor not found" is incorrectly reported instead of actual HTTP errors.
  
- If the script exits without an error, it implies that `linkcheck` reported the HTTP error as expected, suggesting that the issue might have been resolved in the Sphinx version you are using.

Remember, the effectiveness of this script relies on the accuracy of the expected error message fragment it checks for. Adjustments might be needed based on the actual output of your Sphinx `linkcheck` command or environment differences.