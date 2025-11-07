Below is the `reproducer.py` script tailored to reproduce the issue where LaTeX inline code highlighting from Sphinx feature #10251 adds unwanted whitespace at the start and end in the PDF output. The script automates the process of:

1. Generating a minimal Sphinx project with a `.rst` file that includes your described inline code and a Python code block.
2. Running the Sphinx build to generate a LaTeX document.
3. Examining the generated `.tex` file for spaces that should not exist around inline code when rendered to PDF.

```python
import os
import subprocess
import sys

def create_minimal_sphinx_project():
    os.makedirs('test_project/source', exist_ok=True)
    with open('test_project/source/conf.py', 'w') as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    with open('test_project/source/index.rst', 'w') as f:
        f.write(".. role:: python(code)\n")
        f.write("   :language: python\n")
        f.write("   :class: highlight\n")
        f.write("\n")
        f.write("Inline :python:`def foo(1 + 2 + None + \"abc\"): pass` code block\n")
        f.write("\n")
        f.write(".. code-block:: python\n")
        f.write("\n")
        f.write("   def foo(1 + 2 + None + \"abc\"): pass\n")

def build_latex():
    subprocess.run(["sphinx-build", "-b", "latex", "test_project/source", "test_project/build"], check=True)

def check_for_unwanted_whitespace():
    tex_file_path = 'test_project/build/index.tex'
    with open(tex_file_path, 'r') as f:
        contents = f.read()
    expected_content_without_spaces = r'\sphinxcode{\sphinxupquote{%def foo(1 + 2 + None + "abc"): pass%}}'
    if expected_content_without_spaces in contents:
        print("Issue fixed.")
        sys.exit(0)
    else:
        raise AssertionError("Unwanted whitespace found around inline code in LaTeX output.")

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

def main():
    try:
        create_minimal_sphinx_project()
        build_latex()
        check_for_unwanted_whitespace()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

To use this script:
1. Ensure you have Sphinx installed in your python environment (`pip install sphinx`).
2. Save the script as `reproducer.py` in the root directory of your Sphinx project.
3. Execute it using `python3 reproducer.py`.

The script will:
- Exit with code 0 and print "Issue fixed." if the unwanted whitespace issue is no longer present.
- Print a stack trace and exit with a non-zero code if the issue persists, which helps in diagnosing the problem.