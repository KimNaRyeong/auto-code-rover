The following `reproducer.py` script aims to automatically reproduce the described linting issue. It creates the directory and file structure required, attempts to run `pylint` on the created files, and checks for expected and actual outcomes to assert the presence of the issue. The script cleans up after itself to avoid leaving unnecessary files or directories on the system.

```python
import subprocess
import os
from pathlib import Path

def setup_environment():
    """
    Creates the directory and file structure for the test.
    """
    os.makedirs("a", exist_ok=True)
    Path("a/a.py").touch()
    Path("a/b.py").touch()
    Path("r.py").write_text("from a import b")

def run_pylint(target):
    """
    Runs pylint on the specified target and returns the output.
    """
    result = subprocess.run(["pylint", target], capture_output=True, text=True)
    return result

def cleanup_environment():
    """
    Cleans up files and directories created for the test.
    """
    Path("a/a.py").unlink()
    Path("a/b.py").unlink()
    os.rmdir("a")
    Path("r.py").unlink()

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
    
def test_linting_issue():
    setup_environment()
    
    try:
        # Test the first scenario
        result = run_pylint("a")
        assert "F0010" not in result.stderr, "Linting failed due to missing __init__.py"

        # Test the second scenario involving module resolution side-effects
        result = run_pylint("-E r a")
        assert "E0611" not in result.stderr and "F0010" not in result.stderr, "Linting failed on module resolution"

    except AssertionError as e:
        print_stacktrace(e)
        raise
    finally:
        cleanup_environment()

if __name__ == "__main__":
    test_linting_issue()
```

This script does the following:
1. **Setup:** Creates a directory `a` with two Python files `a/a.py` and `a/b.py`, and another Python file `r.py` in the root directory.
2. **Test:** It first checks whether running `pylint a` succeeds without errors related to missing `__init__.py`. Then, it tests module resolution by running `pylint -E r a` to see if there are import-related linting errors or parse errors.
3. **Cleanup:** Removes the created files and directory to restore the environment.

When you run this script, it should raise an `AssertionError` if the issue is present, effectively providing a stack trace of where in your script the issue was detected. When the issue with `pylint` is resolved, the script should exit with code 0, indicating success with no exceptions raised.