To design a `reproducer.py` script capable of validating the described LaTeX issue, we must simulate the steps that lead to the production of LaTeX output along with the spaces around inline code blocks. This requires us to programmatically create a minimal Sphinx project, generate LaTeX output, and examine that output for the unwanted spaces. Given the specific nature of this issue, it's important to note that directly reproducing the LaTeX formatting issue just with Python may not fully encapsulate the LaTeX compilation process, but we can attempt to reproduce the steps leading up to it.

```python
import os
import subprocess
import shutil

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

def create_minimal_sphinx_project():
    os.mkdir('test_project')
    with open('test_project/conf.py', 'w') as conf:
        conf.write("project = 'Test Project'\n")
        conf.write("extensions = ['sphinx.ext.autodoc']\n")
    with open('test_project/index.rst', 'w') as index:
        index.write("""
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
""")

def generate_latex():
    subprocess.run(["sphinx-build", "-b", "latex", "test_project", "test_project/_build/latex"], check=True)

def check_latex_output():
    with open("test_project/_build/latex/testproject.tex", "r") as f:
        content = f.read()
        if "\\sphinxcode{\\sphinxupquote{ def foo(1 + 2 + None + \"abc\"): pass }}" in content:
            raise AssertionError("Inline code highlighting includes unwanted whitespace.")

def cleanup():
    shutil.rmtree('test_project', ignore_errors=True)

if __name__ == "__main__":
    try:
        create_minimal_sphinx_project()
        generate_latex()
        check_latex_output()
        print("Issue not found: inline code highlighting does not include unwanted whitespace.")
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
    finally:
        cleanup()
```

**Note:** This script assumes that Sphinx is installed and can be invoked from the command line with `sphinx-build`. It automates the creation of a minimal Sphinx project, including the `conf.py` and `index.rst` files. Then, it invokes Sphinx to generate LaTeX output and checks this output for the specific issue of spaces around inline code. It cleans up by removing the project directory afterwards. If the LaTeX output matches the problematic output, it raises an `AssertionError`; otherwise, it prints a message indicating the issue was not found. 

Be advised, actual behavior may vary depending on the Sphinx version, the LaTeX setup, and the environment. This script might require adjustments for accurate execution across different platforms.