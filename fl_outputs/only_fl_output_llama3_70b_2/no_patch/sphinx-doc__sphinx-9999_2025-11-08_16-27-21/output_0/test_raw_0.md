Here is the reproducer.py file:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder
from sphinx.writers.latex import LaTeXWriter

def reproduce_issue():
    # Create a temporary directory for the project
    tmp_dir = "tmp_latex_issue"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create a Sphinx project in the temporary directory
    src_dir = os.path.join(tmp_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "index.rst"), "w") as f:
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

    # Build the LaTeX output
    app = Sphinx(src_dir, src_dir, os.path.join(tmp_dir, "latex"), os.path.join(tmp_dir, "doctrees"))
    app.builder = LaTeXBuilder(app)
    app.builder.build_all()

    # Check if the issue is present in the LaTeX output
    latex_output = os.path.join(tmp_dir, "latex", "index.tex")
    with open(latex_output, "r") as f:
        content = f.read()
        if "\\newline" not in content:
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

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
```
This script creates a temporary Sphinx project, builds the LaTeX output, and checks if the terms are separated by a newline in the resulting TeX file. If not, it raises an `AssertionError` with a stack trace of the issue.