import subprocess
import os
import tempfile
import shutil
from typing import Tuple

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

def create_sphinx_project(base_dir: str) -> Tuple[str, str]:
    # Create Sphinx configuration
    conf_py = os.path.join(base_dir, 'conf.py')
    with open(conf_py, 'w') as f:
        f.write("project = 'Demo Project'\n")
        f.write("extensions = []\n")
        f.write("exclude_patterns = ['_build']\n")

    # Create an index.rst file with the problematic code
    index_rst = os.path.join(base_dir, 'index.rst')
    with open(index_rst, 'w') as f:
        f.write(".. c:function:: int foo(int bar)\n\n")
        f.write("   :param int bar: Bar\n")

    return conf_py, index_rst

def check_warning(output: str) -> bool:
    # Define the expected warning message
    expected_warning = "WARNING: Unparseable C cross-reference: 'int'"
    return expected_warning in output

def main():
    try:
        # Create a temporary directory for the Sphinx project
        temp_dir = tempfile.mkdtemp()

        # Set up the Sphinx project
        conf_py, index_rst = create_sphinx_project(temp_dir)

        # Run Sphinx to build the documentation
        result = subprocess.run(['sphinx-build', '-M', 'html', temp_dir, os.path.join(temp_dir, '_build')], capture_output=True, text=True)
        
        # Check for the specific warning in the output
        if not check_warning(result.stdout):
            raise AssertionError("The issue is not present or the warning message has changed: Sphinx did not generate the expected warning.")

        print("Issue reproduced successfully. The expected warning was detected.")

    except Exception as e:
        print_stacktrace(e)
        raise
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
