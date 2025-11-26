I apologize for the previous mistake. Here is a new `reproducer.py` file that should reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.writers.latex import LaTeXWriter
from docutils.core import publish_string

def reproduce_issue():
    rst_content = """
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
"""

    latex_content = publish_string(rst_content, writer_name='latex')

    # Check if the issue is present in the generated LaTeX file
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
This script generates an RST string with the LaTeX code, converts it to LaTeX using `docutils`, and checks if the issue is present in the generated LaTeX file. If the issue is present, it raises an AssertionError with a stack trace of the issue.

Please note that you need to have Sphinx and docutils installed in your environment for this script to work.