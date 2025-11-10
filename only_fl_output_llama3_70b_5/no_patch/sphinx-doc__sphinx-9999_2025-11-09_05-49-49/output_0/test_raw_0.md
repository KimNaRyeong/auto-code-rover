Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder
from sphinx.writers.latex import LaTeXWriter

def reproducer():
    # Create a temporary directory for the project
    tmp_dir = "tmp_latex_issue"
    os.makedirs(tmp_dir, exist_ok=True)
    os.chdir(tmp_dir)

    # Create a sample reStructuredText file
    with open("sample.rst", "w") as f:
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
    app = Sphinx("latex_issue", "latex_issue", "tmp_latex_issue")
    app.builder = LaTeXBuilder(app)

    # Build the LaTeX document
    app.build()

    # Check if the issue is present
    with open("latex_issue.tex", "r") as f:
        latex_content = f.read()
        if "\\newline" not in latex_content:
            raise AssertionError("Terms are not separated by a newline")

    print("Issue is fixed!")

def main():
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
```
This script creates a temporary directory, generates a sample reStructuredText file, builds the LaTeX document using Sphinx, and checks if the issue is present by searching for the `\newline` command in the generated LaTeX content. If the issue is present, it raises an `AssertionError`.