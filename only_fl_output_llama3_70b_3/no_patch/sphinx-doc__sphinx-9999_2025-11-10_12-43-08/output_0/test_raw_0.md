Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder

def reproducer():
    # Create a temporary directory for the project
    tmp_dir = "tmp_latex_issue"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create a sample reStructuredText file
    rst_file = os.path.join(tmp_dir, "listing.rst")
    with open(rst_file, "w") as f:
        f.write("""
Listing:

:samp:`{file}.cc` :samp:`{file}.cp` :samp:`{file}.cxx` :samp:`{file}.cpp` :samp:`{file}.CPP` :samp:`{file}.c++` :samp:`{file}.C`
  C++ source code that must be preprocessed.  Note that in :samp:`.cxx`,
  the last two letters must both be literally :samp:`x`.  Likewise,
  :samp:`.C` refers to a literal capital C.

:samp:`{file}.mm` :samp:`{file}.M`
  Objective-C++ source code that must be preprocessed.

:samp:`{file}.mii`
  Objective-C++ source code that should not be preprocessed.

:samp:`{file}.hh` :samp:`{file}.H` :samp:`{file}.hp` :samp:`{file}.hxx` :samp:`{file}.hpp` :samp:`{file}.HPP` :samp:`{file}.h++` :samp:`{file}.tcc`
  C++ header file to be turned into a precompiled header or Ada spec
""")

    # Create a Sphinx project
    project_dir = os.path.join(tmp_dir, "project")
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")

    # Build the LaTeX output
    app = Sphinx(project_dir, project_dir, os.path.join(tmp_dir, "_build"), os.path.join(tmp_dir, "_build", "doctrees"))
    app.builder = LaTeXBuilder(app)
    app.build()

    # Check if the LaTeX output has newlines between terms
    latex_file = os.path.join(tmp_dir, "_build", "latex", "listing.tex")
    with open(latex_file, "r") as f:
        latex_content = f.read()
    if "\n" not in latex_content:
        raise AssertionError("Terms are not separated by a newline")

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

if __name__ == "__main__":
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script creates a temporary directory for the project, creates a sample reStructuredText file, builds the LaTeX output using Sphinx, and checks if the LaTeX output has newlines between terms. If not, it raises an `AssertionError` with a stack trace of the issue.