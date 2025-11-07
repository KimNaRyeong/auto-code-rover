import os
import subprocess
import sys
import tempfile

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

def run_sphinx_build(source_dir, build_dir):
    cmd = ["sphinx-build", "-W", "-b", "html", source_dir, build_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to build documentation:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise AssertionError("Duplicate term description issue detected.")

def create_sphinx_project(tmp_dir):
    source_dir = os.path.join(tmp_dir, "source")
    build_dir = os.path.join(tmp_dir, "build")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    conf_py = """
project = 'Test Project'
master_doc = 'index'
extensions = []
"""
    index_rst = """
.. toctree::
   :maxdepth: 2
   :caption: Contents:

glossary
"""
    glossary_rst = """
.. glossary::

    mysql
        A relational database management system.

    MySQL
        Another entry for MySQL, differing only by case.
"""

    with open(os.path.join(source_dir, 'conf.py'), 'w') as f:
        f.write(conf_py)
    with open(os.path.join(source_dir, 'index.rst'), 'w') as f:
        f.write(index_rst)
    with open(os.path.join(source_dir, 'glossary.rst'), 'w') as f:
        f.write(glossary_rst)

    return source_dir, build_dir

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir, build_dir = create_sphinx_project(tmpdir)
        try:
            run_sphinx_build(source_dir, build_dir)
            print("No issue detected, exiting with code 0.")
            sys.exit(0)
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == "__main__":
    main()
