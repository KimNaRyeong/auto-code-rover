import subprocess
import os
import sys
import glob

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
    project_dir = "test_project"
    os.makedirs(project_dir, exist_ok=True)
    conf_py = os.path.join(project_dir, "conf.py")
    index_rst = os.path.join(project_dir, "index.rst")
    with open(conf_py, "w") as f:
        f.write("project = 'TestProject'\n")
        f.write("exclude_patterns = ['_build']\n")
        f.write("extensions = ['sphinx.ext.autodoc']\n")  # Ensure this matches your actual Sphinx extensions if needed
        f.write("latex_engine = 'xelatex'\n")  # This should match the engine used in the reported issue
    
    with open(index_rst, "w") as f:
        f.write("""
.. code-block:: rst

    Listing:
    
    :samp:`{file}.cc` :samp:`{file}.cp` :samp:`{file}.cxx` :samp:`{file}.cpp` :samp:`{file}.CPP` :samp:`{file}.c++` :samp:`{file}.C`
      C++ source code that must be preprocessed. Note that in :samp:`.cxx`,
      the last two letters must both be literally :samp:`x`. Likewise,
      :samp:`.C` refers to a literal capital C.
    
    :samp:`{file}.mm` :samp:`{file}.M`
      Objective-C++ source code that must be preprocessed.
    
    :samp:`{file}.mii`
      Objective-C++ source code that should not be preprocessed.
    
    :samp:`{file}.hh` :samp:`{file}.H` :samp:`{file}.hp` :samp:`{file}.hxx` :samp:`{file}.hpp` :samp:`{file}.HPP` :samp:`{file}.h++` :samp:`{file}.tcc`
      C++ header file to be turned into a precompiled header or Ada spec
""")
    return project_dir

def build_and_check_latex(project_dir):
    try:
        subprocess.run(['sphinx-build', '-b', 'latex', project_dir, os.path.join(project_dir, '_build', 'latex')], check=True)
        latex_files = glob.glob(os.path.join(project_dir, '_build', 'latex', '*.tex'))
        if not latex_files:
            raise FileNotFoundError("No LaTeX (.tex) files found in the build directory.")
        for latex_file in latex_files:
            with open(latex_file, 'r') as f:
                content = f.read()
            assert "C++ source code that must be preprocessed." in content, "Expected text not found in LaTeX file."
            assert "\\item[{\\sphinxstyleliteralintitle{\\sphinxupquote{file.cc}}}" in content, "Expected LaTeX separation not found."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def main():
    project_dir = setup_sphinx_project()
    build_and_check_latex(project_dir)
    print("Issue not reproduced. The LaTeX output appears to be correct. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
