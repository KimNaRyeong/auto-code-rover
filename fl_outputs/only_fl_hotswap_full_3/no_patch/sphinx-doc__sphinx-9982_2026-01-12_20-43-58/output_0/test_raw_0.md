 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
import subprocess
import sys
import warnings


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def run_make_html():
    try:
        subprocess.check_call(["make", "html"], cwd="docs")
    except subprocess.CalledProcessError as e:
        return e


def main():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        run_make_html()
        if len(w) != 2:
            print_stacktrace(Exception(f"Expected 2 warnings, got {len(w)}"))
            sys.exit(1)
        for warning in w:
            if "image" in warning.message:
                color = "light red"
            elif "transition" in warning.message:
              