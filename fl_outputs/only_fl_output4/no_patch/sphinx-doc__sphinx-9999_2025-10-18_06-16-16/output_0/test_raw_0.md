Certainly! Below is a standalone Python script designed to reproduce the issue described. This script will attempt to build a minimal Sphinx project that includes the reStructuredText snippet causing the issue. It will then check the generated LaTeX file for the expected behavior (terms separated by a newline in the case of the glossary entries and the absence of unnecessary new lines for the simple indentation issue). If the issue is present, it will raise an `AssertionError` and print a detailed stack trace.

Please ensure you have Sphinx installed in your environment (`pip install sphinx`) before running this script.

```python
import os
import subprocess
import sys

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

def setup_sphinx_project():
    conf_py = """
project = 'Test Project'
master_doc = 'index'
extensions = []
latex_elements = {}
    """

    index_rst = """
.. toctree::

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
    os.makedirs("source", exist_ok=True)
    with open("source/conf.py", "w") as f:
        f.write(conf_py)
    with open("source/index.rst", "w") as f:
        f.write(index_rst)

def build_sphinx_project():
    subprocess.run(["sphinx-build", "-b", "latex", "source", "build"], check=True)

def verify_output():
    output_tex = "build/index.tex"
    with open(output_tex, "r") as f:
        content = f.read()

    # Check for glossary issue
    if "boson\n   Particle with integer spin." not in content:
        raise AssertionError("Glossary terms are not properly separated by newline.")
    
    # Check for the simple indentation issue
    if "samp" in content and "\\newline" not in content:
        raise AssertionError("Latex: terms are not separated by a newline as expected.")

if __name__ == "__main__":
    try:
        setup_sphinx_project()
        build_sphinx_project()
        verify_output()
        print("Issue not found or has been fixed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script performs the following steps:
1. Creates a basic Sphinx project with a single `index.rst` containing the problematic reStructuredText.
2. Configures the Sphinx project with minimal settings required to generate a LaTeX document.
3. Builds the LaTeX document using Sphinx.
4. Checks the generated `.tex` file for the presence of the issue.
5. Raises an `AssertionError` if the issue is detected, printing a detailed stack trace.

Before running the script, ensure Sphinx is correctly installed and accessible in your Python environment. The script assumes the Sphinx `sphinx-build` command is available on the system path.