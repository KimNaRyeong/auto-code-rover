```python
import os
import subprocess
import sys
import tempfile
from typing import List

def setup_test_environment(src_code: str) -> str:
    """
    Sets up a Sphinx documentation testing environment.
    """
    # Create a temporary directory
    dirpath = tempfile.mkdtemp()
    
    # Write the source code to a file
    os.mkdir(os.path.join(dirpath, "api"))
    with open(os.path.join(dirpath, "file.py"), "w") as f:
        f.write(src_code)
    
    # Run sphinx-quickstart with default options, non-interactively
    subprocess.run(["sphinx-quickstart", "--quiet", "--project=test", "--author=test", dirpath],
                   input=b'\n' * 10, text=True)
    
    # Update conf.py
    conf_path = os.path.join(dirpath, "conf.py")
    with open(conf_path, "a") as f:
        f.write("\nimport os\nimport sys\nsys.path.insert(0, os.path.abspath('.'))\n")
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    
    # Update index.rst
    index_path = os.path.join(dirpath, "index.rst")
    with open(index_path, "a") as f:
        f.write("\n.. toctree::\n   :maxdepth: 2\n   :caption: Contents:\n\n")
        f.write("   api/file\n")
    
    # Generate API docs
    subprocess.run(["sphinx-apidoc", "-f", "-o", "api", "."], cwd=dirpath)

    return dirpath

def run_sphinx_build(dirpath: str) -> List[str]:
    """
    Runs Sphinx build and returns the generated HTML file paths.
    """
    # Build the HTML documentation
    subprocess.run(["make", "html"], cwd=dirpath)
    
    html_dir = os.path.join(dirpath, "_build", "html", "api")
    return [os.path.join(html_dir, f) for f in os.listdir(html_dir) if f.endswith('.html')]

def check_html_content(html_files: List[str], search_texts: List[str]) -> None:
    """
    Checks if each of the search_texts is present in at least one of the HTML files.
    Raises an AssertionError if not.
    """
    for text in search_texts:
        if not any(text in open(f).read() for f in html_files):
            raise AssertionError(f"Documentation missing expected text: {text}")

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
    src_code = '''
# file.py
from pathlib import Path
from typing import Any, Callable, Dict, Union

# Signatures for the documentation purposes

ScaffoldOpts = Dict[str, Any]
"""Dictionary with PyScaffold's options, see ``pyscaffold.api.create_project``.
Should be treated as immutable (if required, copy before changing).

Please notice some behaviours given by the options **SHOULD** be observed. For example,
files should be overwritten when the **force** option is ``True``. Similarly when
**pretend** is ``True``, no operation should be really performed, but any action should
be logged as if realized.
"""

FileContents = Union[str, None]
"""When the file content is ``None``, the file should not be written to
disk (empty files are represented by an empty string ``""`` as content).
"""

FileOp = Callable[[Path, FileContents, ScaffoldOpts], Union[Path, None]]
"""Signature of functions considered file operations::

    Callable[[Path, FileContents, ScaffoldOpts], Union[Path, None]]

- **path** (:obj:`pathlib.Path`): file path potentially to be written to/changed
  in the disk.
- **contents** (:obj:`FileContents`): usually a string that represents a text content
  of the file. :obj:`None` indicates the file should not be written.
- **opts** (:obj:`ScaffoldOpts`): a dict with PyScaffold's options.

If the file is written (or more generally changed, such as new access permissions),
by convention they should return the :obj:`file path <pathlib.Path>`.
If no file was touched, :obj:`None` should be returned. Please notice a **FileOp**
might return :obj:`None` if a pre-existing file in the disk is not modified.

.. note::
    A **FileOp** usually has side effects (e.g. write a file to the disk), see
    :obj:`FileFileContents` and :obj:`ScaffoldOpts` for other conventions.
"""
'''

    try:
        dirpath = setup_test_environment(src_code)
        html_files = run_sphinx_build(dirpath)
        check_html_content(
            html_files,
            [
                "Dictionary with PyScaffold's options",
                "When the file content is ``None``",
                "Signature of functions considered file operations",
            ]
        )
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Test passed, HTML documentation contains all expected docstrings.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```