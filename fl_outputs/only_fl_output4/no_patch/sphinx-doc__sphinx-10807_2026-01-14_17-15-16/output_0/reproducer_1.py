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

def main():
    project_dir = 'test_project'
    os.makedirs(project_dir, exist_ok=True)
    mod_file_path = os.path.join(project_dir, 'mod.py')

    # Create a simple module with a function
    with open(mod_file_path, 'w') as mod_file:
        mod_file.write('''"""
Subheader
---------
"""
def my_function():
    """Function docstring"""
    pass
''')

    # Create a minimal Sphinx conf.py
    conf_py = os.path.join(project_dir, 'conf.py')
    with open(conf_py, 'w') as conf_file:
        conf_file.write('''import os
import sys
sys.path.insert(0, os.path.abspath('.'))
project = 'TestProject'
extensions = ['sphinx.ext.autodoc']
master_doc = 'index'
html_theme = 'alabaster'
''')

    # Create an index.rst with automodule directive
    index_rst = os.path.join(project_dir, 'index.rst')
    with open(index_rst, 'w') as index_file:
        index_file.write('''Test Module Documentation
==========================

.. automodule:: mod
    :members:
''')

    # Run Sphinx to build the docs
    process = subprocess.run(['sphinx-build', '-b', 'html', project_dir, os.path.join(project_dir, '_build')], capture_output=True, text=True)
    if process.returncode != 0:
        print(process.stdout, file=sys.stderr)
        print(process.stderr, file=sys.stderr)
        sys.exit(1)

    # Check if the issue exists by analysing the generated HTML
    html_output_path = os.path.join(project_dir, '_build', 'index.html')
    try:
        with open(html_output_path, 'r') as html_file:
            html_content = html_file.read()
            assert 'Subheader' not in html_content, "Content under 'Subheader' found in index.html, indicating potential issue."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Issue not present or fixed.")
    sys.exit(0)

if __name__ == '__main__':
    main()
