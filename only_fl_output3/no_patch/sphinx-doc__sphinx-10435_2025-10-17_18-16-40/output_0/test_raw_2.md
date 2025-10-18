Creating a standalone Python script `reproducer.py` that you can execute in your project's root directory to reproduce the given LaTeX issue involves programmatically generating a minimal Sphinx project, compiling it to LaTeX, and then checking the generated `.tex` file for unexpected spaces around inline code blocks. This script would ideally need Sphinx and its dependencies installed in the executing environment. I'll assume Sphinx and docutils are correctly set up.

The script outlined below handles setting up a minimal Sphinx environment, building the LaTeX output, and then examining the LaTeX file for the specified issue. If the issue is present—an unexpected space around inline code blocks—the script will raise an `AssertionError`. Conversely, if the issue is fixed, it will exit with code 0 without any exception.

```python
import os
import subprocess
import sys
import shutil

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

def create_sphinx_project():
    # Create directories
    os.makedirs('test_project/source', exist_ok=True)
    os.makedirs('test_project/build', exist_ok=True)
    
    # Create conf.py
    conf_content = """\
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

extensions = []
templates_path = ['_templates']
exclude_patterns = []

project = 'Sphinx Issue Test'
master_doc = 'index'
latex_elements = {}
"""
    
    # Create index.rst
    index_content = """\
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python
    
    def foo(1 + 2 + None + "abc"): pass
"""
    
    with open('test_project/source/conf.py', 'w') as f:
        f.write(conf_content)
    
    with open('test_project/source/index.rst', 'w') as f:
        f.write(index_content)

def build_latex():
    try:
        subprocess.run([sys.executable, '-m', 'sphinx', '-b', 'latex', 'test_project/source', 'test_project/build'], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to build LaTeX document.")
        print_stacktrace(e)
        sys.exit(1)

def check_issue():
    with open('test_project/build/TestDoc.tex', 'r') as f:
        content = f.read()
        if " \PYG" in content or "\PYG " in content:
            raise AssertionError("Unintended whitespace found around inline code blocks.")

if __name__ == '__main__':
    try:
        create_sphinx_project()
        build_latex()
        check_issue()
        print("No issue detected.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Clean up
        shutil.rmtree('test_project', ignore_errors=True)
```

Please keep in mind, depending on the Sphinx version and setup, the generated LaTeX file name or path might differ (for example, `TestDoc.tex` might not match exactly what your Sphinx version produces). Adjust the script accordingly to target the correct `.tex` file in the `check_issue` function. Additionally, ensure that any needed Sphinx extensions or configurations specific to reproducing the issue are included in the `conf_content` string.