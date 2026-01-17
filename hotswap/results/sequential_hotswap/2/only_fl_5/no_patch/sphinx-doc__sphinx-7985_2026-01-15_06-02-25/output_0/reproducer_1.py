import subprocess
import os
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

def setup_sphinx_project():
    os.makedirs("test_project/_static", exist_ok=True)
    os.makedirs("test_project/_templates", exist_ok=True)
    with open("test_project/conf.py", "w") as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = ['sphinx.ext.linkcheck']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static']
""")
    with open("test_project/index.rst", "w") as f:
        f.write("""
Welcome to test_project's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
""")

def run_linkcheck():
    try:
        setup_sphinx_project()
        result = subprocess.run(["sphinx-build", "-b", "linkcheck", "test_project", "test_project/_build/linkcheck"],
                                capture_output=True, text=True)
        if result.returncode == 0 and "local-link" in result.stdout:
            print("Local link was checked by linkcheck, script exits with code 0.")
            sys.exit(0)
        else:
            raise AssertionError("Local link was not checked by linkcheck.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Cleanup to remove the test_project directory after running the test
        subprocess.run(["rm", "-rf", "test_project"])

if __name__ == "__main__":
    run_linkcheck()
