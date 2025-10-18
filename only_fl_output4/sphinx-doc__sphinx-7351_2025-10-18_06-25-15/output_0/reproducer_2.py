import os
import subprocess
import shutil
from tempfile import TemporaryDirectory

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

def create_sphinx_project(temp_dir):
    index_content = """
.. toctree::
   a
"""
    a_md_content = """
# MD Title

MD content should be included.
"""
    a_rst_content = """
RST Title
=========

RST content should *not* be included if `a.md` is properly recognized.
"""
    with open(os.path.join(temp_dir, 'index.rst'), 'w') as f:
        f.write(index_content)
    with open(os.path.join(temp_dir, 'a.md'), 'w') as f:
        f.write(a_md_content)
    with open(os.path.join(temp_dir, 'a.rst'), 'w') as f:
        f.write(a_rst_content)

    conf_py_content = """
extensions = ['myst_parser']
"""
    with open(os.path.join(temp_dir, 'conf.py'), 'w') as f:
        f.write(conf_py_content)

def run_sphinx_build(temp_dir):
    try:
        subprocess.check_call(['sphinx-build', '-b', 'html', temp_dir, os.path.join(temp_dir, '_build')])
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("Sphinx build failed")

def check_build_output(temp_dir):
    output_path = os.path.join(temp_dir, '_build', 'index.html')
    if not os.path.exists(output_path):
        raise AssertionError("Build output not found. Please check if Sphinx build was successful and output path is correct.")
    with open(output_path, 'r') as f:
        content = f.read()
        if "MD content should be included." not in content:
            raise AssertionError("The build does not include content from `a.md` as expected.")

def main():
    with TemporaryDirectory() as temp_dir:
        create_sphinx_project(temp_dir)
        run_sphinx_build(temp_dir)
        check_build_output(temp_dir)
        print("Test passed: a.md content is correctly included.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
