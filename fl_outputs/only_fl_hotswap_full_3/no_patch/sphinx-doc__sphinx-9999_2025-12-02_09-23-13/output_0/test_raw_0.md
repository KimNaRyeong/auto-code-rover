 Here is a standalone Python script `reproducer.py` that uses the Sphinx library to reproduce the issue:

```python
import sys
from docutils.writers.latex2e import LaTeX2EWriter

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

# Define the problematic listing
listing = """\
Listing:

:samp:`{file}.cc` :samp:`{file}.cp` :samp:`{file}.cxx` :samp:`{file}.cpp` :samp:`{file}.CPP` :samp:`{file}.c++` :samp:`{file}.C` \\
  C++ source code that must be preprocessed.  Note that in :samp:`.cxx`, \\
  the last two letters must both be literally :samp:`x`.  Likewise, \\
  :samp:`.C` refers to a literal capital C. \\

:samp:`{file}.mm` :samp:`{file}.M` \\
  Objective-C++ source code that must be preprocessed. \\

:samp:`{file}.mii` \\
  Objective-C++ source code that should not be preprocessed. \\

:samp:`{file}.hh` :samp:`{file}.H` :samp:`{file}.hp` :samp:`{file}.hxx` :samp:`{file}.hpp` :samp:`{file}.HPP` :samp:`{file}.h++` :samp:`{file}.tcc` \\
  C++ header file to be turned into a precompiled header or Ada spec \\
"""

# Define the problematic glossary
glossary = """\
.. glossary:: \\
   :sorted: \\

   boson \\
      Particle with integer spin. \\

   *fermion* \\
      Particle with half-integer spin. \\

   tauon \\
   myon \\
   electron \\
      Examples for fermions. \\

   über \\
      Gewisse \\
"""

# Initialize Sphinx
sys.path.insert(0, ".")
import sphinx
app = sphinx.application.Sphinx(srcdir=".", confdir=".", doctreedir="doctreedir", buildername="latex", warningiserror=True)

# Write the problematic listing and glossary to temporary files
with open("listing.rst", "w") as f:
    f.write(listing)
with open("glossary.rst", "w") as f:
    f.write(glossary)

# Create a LaTeX writer
latex_writer = LaTeX2EWriter(app)

# Write the LaTeX output for the problematic listing and glossary
with open("listing.tex", "w") as f:
    latex_writer.write(app.builder.get_outdated_docs(), app.env, "listing", system_messages=app.builder.warn_messages, out=f)
with open("glossary.tex", "w") as f:
    latex_writer.write(app.builder.get_outdated_docs(), app.env, "glossary", system_messages=app.builder.warn_messages, out=f)

# Check if the LaTeX output contains newlines between terms
with open("listing.tex", "r") as f:
    lines = f.readlines()
    if len(lines) > 1 and lines[-2] != "\\\\\n":
        raise AssertionError("Terms in listing are not separated by a newline")

with open("glossary.tex", "r") as f: