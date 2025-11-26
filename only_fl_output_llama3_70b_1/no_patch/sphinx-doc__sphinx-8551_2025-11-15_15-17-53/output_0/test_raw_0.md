Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.docutils import docutils_namespace

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

def test_issue():
    # Create a temporary directory for the project
    tmp_dir = "tmp_sphinx_project"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the Sphinx project structure
    os.makedirs(os.path.join(tmp_dir, "source"), exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, "build"), exist_ok=True)

    # Create the conf.py file
    with open(os.path.join(tmp_dir, "source", "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")

    # Create the index.rst file
    rst_content = """
.. py:currentmodule:: mod

.. py:class:: A

.. py:function:: f()

  - :py:class:`A`
  - :py:class:`mod.A`
  - :py:class:`mod.submod.A`

:param A a:
:param mod.A b:
:param mod.submod.A c:
:rtype: A
:rtype: mod.A
:rtype: mod.submod.A

.. py:currentmodule:: mod.submod

.. py:class:: A

.. py:function:: f()

  - :py:class:`A`
    with open(os.path.join(tmp_dir, "source", "index.rst"), "w") as f:
        f.write(rst_content)

    # Build the Sphinx project
    app = Sphinx(srcdir=tmp_dir, confdir=tmp_dir, outdir=os.path.join(tmp_dir, "build"))
    app.builder = StandaloneHTMLBuilder(app)
    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    # Check if the issue is fixed
    with open(os.path.join(tmp_dir, "build", "index.html"), "r") as f:
        html_content = f.read()
        if "mod.A" in html_content and "mod.submod.A" not in html_content:
            raise AssertionError("Issue is present")

    print("Issue is fixed")

if __name__ == "__main__":
    test_issue()
```
This script creates a temporary Sphinx project, builds it, and checks if the issue is present by searching for the incorrect link target in the generated HTML file. If the issue is present, it raises an `AssertionError` with a stack trace.