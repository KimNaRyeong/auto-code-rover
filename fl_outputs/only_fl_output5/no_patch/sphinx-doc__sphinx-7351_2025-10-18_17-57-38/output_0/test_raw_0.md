Here is a standalone Python script named `reproducer.py` that aims to set up a minimal Sphinx project, add the given files, and run a Sphinx build to check if the issue described can be reproduced. This script assumes you have Sphinx and necessary extensions installed in your Python environment.

```python
import os
from sphinx.application import Sphinx
from sphinx.util.docutils import sphinx_domains
import shutil

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

def setup_sphinx_project(srcdir, confdir, outdir, doctreedir):
    os.makedirs(srcdir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(doctreedir, exist_ok=True)

    with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
        f.write('.. toctree::\n    a.md\n')

    with open(os.path.join(srcdir, 'a.rst'), 'w') as f:
        f.write('This is a.rst')

    with open(os.path.join(srcdir, 'a.md'), 'w') as f:
        f.write('This is a.md')

    with open(os.path.join(confdir, 'conf.py'), 'w') as f:
        f.write("extensions = ['myst_parser']\n")

def run_sphinx(srcdir, confdir, outdir, doctreedir):
    app = Sphinx(srcdir, confdir, outdir, doctreedir, 'html')
    app.build(force_all=True)
    return app

def check_issue(app):
    with open(os.path.join(app.outdir, 'index.html'), 'r') as f:
        content = f.read()
        # Assuming 'This is a.md' should be in the content if `a.md` was included.
        if 'This is a.md' not in content:
            raise AssertionError("a.md was not included as expected.")

def main():
    project_dir = 'test_project'
    srcdir = os.path.join(project_dir, 'source')
    confdir = srcdir  # Configuration directory is the same as source directory in this setup
    outdir = os.path.join(project_dir, 'build')
    doctreedir = os.path.join(project_dir, 'doctrees')

    try:
        setup_sphinx_project(srcdir, confdir, outdir, doctreedir)
        app = run_sphinx(srcdir, confdir, outdir, doctreedir)
        check_issue(app)
        print("The issue seems to be fixed.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

    finally:
        # Cleanup: Uncomment the next line if you do not want to keep the test project after running this script.
        # shutil.rmtree(project_dir)

if __name__ == "__main__":
    main()
```
This script:

1. Sets up a minimal Sphinx project with the given file structure.
2. Builds the project.
3. Checks if `a.md` was correctly included in the build output.

Upon running this script with `python3 reproducer.py`, it will:
- Print a stack trace if it encounters an `AssertionError` which indicates the issue is present.
- Print a success message and exit with a 0 code if the issue is not found, which means `a.md` was correctly prioritized over `a.rst`.

**Note:** Make sure to have Sphinx (`pip install sphinx`) and `myst_parser` (`pip install myst-parser`) installed in your Python environment before running the script. This script does not handle Python environment setup or dependency installation.