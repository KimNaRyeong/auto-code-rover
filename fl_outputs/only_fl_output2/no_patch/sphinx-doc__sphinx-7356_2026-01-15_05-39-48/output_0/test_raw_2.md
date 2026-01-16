To address the scenario, the adjusted script below aims to directly reproduce the issue described: changes in fragment identifiers for Python functions documented with Sphinx, resulting from underscores being replaced by dashes. This script no longer depends on the presence of `sphinx-build` in the environment's PATH, but instead directly uses Sphinx's Python API to build the documentation, which more cleanly isolates and demonstrates the behavior. 

This approach necessitates Sphinx to be installed in the Python environment where the script runs. The script creates a minimal Sphinx project with a single Python function documented, triggers a Sphinx build using the Sphinx API, then checks the generated HTML file for the expected anchor format. An `AssertionError` is raised if the modified (dashed) anchor is used, indicating the presence of the issue, or it passes silently if the original (underscored) anchor format is preserved, showing the problem is fixed or not present.

```python
import os
import shutil
import sphinx.application
from io import StringIO

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

def setup_sphinx_project():
    if os.path.exists("test_project"):
        shutil.rmtree("test_project")
    os.makedirs("test_project")
    with open("test_project/conf.py", "w") as f:
        f.write("""
project = 'Test Project'
master_doc = 'index'
html_theme = 'alabaster'
""")
    with open("test_project/index.rst", "w") as f:
        f.write("""
.. py:function:: example_python_function(foo)

   Some function.
""")


def build_sphinx():
    srcdir = os.path.abspath("test_project")
    confdir = srcdir
    outdir = os.path.join(srcdir, "_build")
    doctreedir = os.path.join(outdir, "doctrees")

    sphinx_args = [
        "-b", "html",
        "-d", doctreedir,
        "-W",  # Turn warnings into errors
        srcdir,
        outdir
    ]

    app = sphinx.application.Sphinx(
        srcdir, confdir, outdir, doctreedir, "html",
        warningiserror=True,
        status=StringIO(),
        freshenv=True,
    )
    app.build(force_all=True)

def check_documentation():
    with open("test_project/_build/index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        # Check if the new anchor format is used
        assert "example-python-function" not in contents, \
            "Anchor format changed: underscores replaced with dashes."

def main():
    try:
        setup_sphinx_project()
        build_sphinx()
        check_documentation()
        print("Success: The issue is not present.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Optional: Cleanup project directory after run
        shutil.rmtree("test_project", ignore_errors=True)

if __name__ == "__main__":
    main()
```

**Environment Setup**
Before running this script, ensure you have Sphinx installed in your Python environment (`pip install sphinx`). The script dynamically generates the necessary Sphinx project structure, executes the build process using Sphinx's API, and evaluates the resulting HTML for the issue.

**Note:** Depending on changes in Sphinx or related tools/environment, modifications to this script might be necessary to accurately reproduce or check for the discussed issue in future versions.