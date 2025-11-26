Here is the reproducer.py file:
```
import os
from sphinx.application import Sphinx

def reproduce_issue():
    # Create a temporary directory for the project
    tmp_dir = "tmp_reproduce_latex_issue"
    os.makedirs(tmp_dir, exist_ok=True)

    # Create a conf.py file with the necessary configuration
    with open(os.path.join(tmp_dir, "conf.py"), "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo']\n")
        f.write("master_doc = 'index'\n")

    # Create an index.rst file with the LaTeX code
    with open(os.path.join(tmp_dir, "index.rst"), "w") as f:
        f.write("""
.. glossary::

   :sorted:

   boson
      Particle with integer spin.

   *fermion*
      Particle with half-integer spin.

   tauon
   myon
   electron
      Examples for fermions.

   über
      Gewisse

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

    # Build the LaTeX document
    app = Sphinx(tmp_dir, tmp_dir, "latex", "index")
    app.build()

    # Check if the issue is present in the generated LaTeX file
    latex_file = os.path.join(tmp_dir, "latex", "index.tex")
    with open(latex_file, "r") as f:
        latex_content = f.read()
        if "\\newline" not in latex_content:
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
    exit(1)
```
This script creates a temporary directory for the project, generates an index.rst file with the LaTeX code, builds the LaTeX document using Sphinx, and checks if the issue is present in the generated LaTeX file. If the issue is present, it raises an AssertionError with a stack trace of the issue.