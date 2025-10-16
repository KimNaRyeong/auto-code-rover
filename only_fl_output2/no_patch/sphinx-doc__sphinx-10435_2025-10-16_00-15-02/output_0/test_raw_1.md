Creating a standalone Python script to reproduce the issue described involves several adjustments from the previous attempt, notably ensuring that `sphinx-build` is accessible in the environment where the script runs. However, it's crucial to remember that the environment must have Sphinx installed, and this script presumes the `sphinx-build` command is available in the system's PATH. If it is not, the same error will occur. Here’s an improved approach:

```python
import subprocess
import sys
import os

def setup_sphinx_project():
    # Ensure the source and build directories exist
    os.makedirs('test_project/source', exist_ok=True)
    os.makedirs('test_project/build', exist_ok=True)
    
    with open('test_project/source/conf.py', 'w') as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
        
    with open('test_project/source/index.rst', 'w') as f:
        f.writelines([
            ".. role:: python(code)\n",
            "   :language: python\n",
            "   :class: highlight\n\n",
            "Inline :python:`def foo(1 + 2 + None + \"abc\"): pass` code block\n\n",
            ".. code-block:: python\n\n",
            "   def foo(1 + 2 + None + \"abc\"): pass\n"
        ])

def build_latex():
    # Running Sphinx build
    try:
        subprocess.run(["sphinx-build", "-b", "latex", "test_project/source", "test_project/build"], 
                       check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)
    
def check_tex_output_for_spaces():
    tex_file_path = os.path.join('test_project/build', next(os.walk('test_project/build'))[2][0])
    with open(tex_file_path, 'r') as f:
        contents = f.read()
    
    if r'\sphinxupquote{%' in contents and r'%}' in contents:
        print("No unwanted whitespace found. Issue may be fixed.")
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
        print(f"    Line {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        setup_sphinx_project()
        build_latex()
        check_tex_output_for_spaces()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Please ensure:
- Sphinx is properly installed and `sphinx-build` is available in your PATH. You can verify this by running `sphinx-build --version` in your terminal.
- You have the necessary permissions to create directories and files when running this script.
- Adjust `check_tex_output_for_spaces()` if the logic for identifying the issue requires more precision or additional context. This script assumes the presence of specific LaTeX macros around inline code without spaces as an indicator of the issue being addressed.