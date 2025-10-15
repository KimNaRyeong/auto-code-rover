```python
import os
import subprocess
import sys

def setup_test_environment():
    """Set up a simple Sphinx project environment to reproduce the issue."""
    os.makedirs('test_project', exist_ok=True)
    with open('test_project/conf.py', 'w') as f:
        f.write("extensions = ['myst_parser']")
    with open('test_project/index.rst', 'w') as f:
        f.write(".. toctree::\n   a.md\n")
    with open('test_project/a.md', 'w') as f:
        f.write("# Markdown file\nSome content.")
    with open('test_project/a.rst', 'w') as f:
        f.write(".. _a rst file:\n\nA reStructuredText file\n----------------------\n\nSome content.")

def build_sphinx():
    """Build the Sphinx documentation."""
    result = subprocess.run(['sphinx-build', '-b', 'html', 'test_project', 'test_project/_build'],
                            capture_output=True, text=True)
    return result

def check_build_output(result):
    """Check the build output for any signs of the issue."""
    if 'WARNING' not in result.stderr:
        raise AssertionError("Expected a warning about the duplicate file names with different extensions.")

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
        setup_test_environment()
        result = build_sphinx()
        check_build_output(result)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issues detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script works under the assumption that you have Sphinx and the `myst_parser` extension installed in your Python environment. You can install Sphinx and `myst_parser` using pip if you haven't already:
```
pip install sphinx myst-parser
```

This script, `reproducer.py`, aims to reproduce the issue mentioned, where Sphinx silently chooses one file to parse when there are multiple files with the same name but different extensions. It sets up a minimal Sphinx project with an `index.rst` file that references `a.md`. There are two files, `a.md` and `a.rst`, with the same base name but different extensions. The script then attempts to build the Sphinx documentation and checks the build output for any warnings regarding duplicate file names with different extensions. If the script detects the issue, it will raise an `AssertionError` and print a stack trace.