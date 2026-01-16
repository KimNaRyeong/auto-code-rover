import os
import subprocess
import sys

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

def create_test_files():
    os.makedirs("docs", exist_ok=True)
    os.makedirs("mod", exist_ok=True)
    with open("docs/conf.py", "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    with open("docs/index.rst", "w") as f:
        f.write(".. automodule:: mod\n   :members:\n")
    with open("mod/__init__.py", "w") as f:
        f.write('''"""
My Module
=========

This is the module docstring

Subheader
---------

.. autosummary::
   :toctree:

   function
"""

def function():
    """My Function"""
    pass
''')

def build_docs():
    subprocess.run(["sphinx-build", "-b", "html", "docs", "docs/_build"], check=True)

def check_for_issue():
    with open("docs/_build/index.html") as f:
        content = f.read()
        if "Subheader" not in content or "function" in content.split("Subheader")[1]:
            raise AssertionError("TOC issue detected")

def main():
    create_test_files()
    try:
        build_docs()
        check_for_issue()
        print("No issue detected, the document structure appears as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(2)

if __name__ == "__main__":
    main()
