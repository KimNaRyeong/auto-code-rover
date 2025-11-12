Here is the `reproducer.py` file that reproduces the issue:
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

def reproduce_issue():
    os.chdir("doc")
    subprocess.check_call(["pip", "install", "Sphinx"])
    try:
        subprocess.check_call(["make", "html"])
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert "duplicate term description of mysql" in str(e), "Issue not reproduced"
    else:
        print("Issue not present")

if __name__ == "__main__":
    reproduce_issue()
```
<|start_header_id|>