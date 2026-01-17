```python
# reproducer.py
import logging
import subprocess
import sys
import tempfile

def run_test_script():
    content = """import logging

import pytest


def _check_cond():
    logging.warning("_check_cond")
    return True


@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")

    assert False
"""
    with tempfile.NamedTemporaryFile("w+", suffix=".py") as tmp_script:
        tmp_script.write(content)
        tmp_script.flush()
        result = subprocess.run(["pytest", tmp_script.name], capture_output=True, text=True)
        return result.stderr, result.stdout

def find_duplicate_log(stderr, stdout):
    if stderr.count("WARNING:root:Schmift") > 0 and "Captured log call" in stdout:
        raise AssertionError("Detected duplicate logging to stderr and captured log")

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
    try:
        stderr, stdout = run_test_script()
        find_duplicate_log(stderr, stdout)
        print("No issue; the logging capture operates as expected.", file=sys.stderr)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```