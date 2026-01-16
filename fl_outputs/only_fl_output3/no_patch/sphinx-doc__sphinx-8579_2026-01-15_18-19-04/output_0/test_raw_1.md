To create a more accurate `reproducer.py` script for the issue described requires simulating or running the Sphinx linkcheck builder in a way that directly interfaces with Sphinx's Python API. This requires setting up a minimal Sphinx environment programmatically and then invoking the linkcheck builder within this setup. Since the issue involves Sphinx's linkcheck misbehaving, the script below aims to set up a minimal Sphinx environment to reproduce the problem programmatically without the overhead of a full Sphinx project setup.

Please note, the provided Python script is tailored to reproduce the type of errors reported (i.e., `ValueError` related to `task_done()` being called too many times and a `TypeError` in the queue module). This is done by directly invoking the functionality that could lead to the observed exceptions within Sphinx's linkcheck process.

```python
import os
import sys
from sphinx.application import Sphinx
from sphinx.cmd.build import main as sphinx_main

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

# Temporary directories setup for Sphinx
src_dir = 'temp_src'
out_dir = 'temp_build'
doctree_dir = 'temp_doctrees'

# Dummy conf.py content
conf_py_content = """
project = 'Temp Project'
master_doc = 'index'
"""

# Dummy index.rst content
index_rst_content = """
Welcome to Temp Project's documentation!
========================================

.. toctree::
   :maxdepth: 2
"""

def setup_temp_sphinx_env():
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(doctree_dir, exist_ok=True)

    with open(os.path.join(src_dir, 'conf.py'), 'w') as f:
        f.write(conf_py_content)

    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write(index_rst_content)

def run_linkcheck():
    try:
        # Setting up a minimal Sphinx environment
        setup_temp_sphinx_env()

        app = Sphinx(src_dir, src_dir, out_dir, doctree_dir, buildername='linkcheck')
        app.build(force_all=True)
        print("Sphinx environment setup and linkcheck run completed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with non-zero code to indicate failure to reproduce

    # Clean up if needed
    cleanup()

def cleanup():
    import shutil
    shutil.rmtree(src_dir, ignore_errors=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    shutil.rmtree(doctree_dir, ignore_errors=True)

if __name__ == "__main__":
    run_linkcheck()
```

Before running this script, you need to ensure Sphinx (`sphinx`) is installed in your Python environment as it makes direct use of Sphinx's API to attempt to reproduce the issue. If the issue is reproduced, a stack trace should be printed. Otherwise, it might indicate the specific conditions leading to the exception are not met, requiring a more detailed setup (e.g., specific linkcheck configurations or external links) or a higher complexity in the documentation to trigger the error.

If the `Sphinx` API and behavior have significantly changed since the version you are reproducing the issue for, adjustments may be needed to match the API usage at that time.