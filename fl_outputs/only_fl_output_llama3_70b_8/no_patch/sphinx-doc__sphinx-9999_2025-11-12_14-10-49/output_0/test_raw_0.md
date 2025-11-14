Here is the reproducer.py file:
```
import os
from sphinx.application import Sphinx

def reproduce_issue():
    # Create a temporary directory for the project
    tmp_dir = "tmp_reproduce_issue"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create the reStructuredText file
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

    # Create the conf.py file
    conf_file = os.path.join(tmp_dir, "conf.py")
    with open(conf_file, "w") as f:
        f.write("extensions = ['sphinx.ext.latex']\n")

    # Build the LaTeX document
    app = Sphinx(tmp_dir, tmp_dir, tmp_dir, tmp_dir)
    app.build()

    # Check if the issue is present in the generated LaTeX file
    latex_file = os.path.join(tmp_dir, "latex", "listing.tex")
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

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
```
This script creates a temporary directory for the project, generates an reStructuredText file with the given content, builds the LaTeX document using Sphinx, and checks if the issue is present in the generated LaTeX file. If the issue is present, it raises an `AssertionError` with a stack trace of the issue.