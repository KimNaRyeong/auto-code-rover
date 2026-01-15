To create a standalone Python script `reproducer.py` that replicates the reported issue, we need to programmatically achieve what was described: creating a minimal Sphinx project, adding an RST document with both working and broken links (external and local), running the Sphinx linkcheck, and verifying if local links are ignored. The script below attempts to automate this process, with an assertion to check if the issue is present (no check for the local link).

```python
import subprocess
import os
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

def create_sphinx_project(project_name: str) -> Tuple[str, str]:
    """
    Creates a minimal Sphinx project using sphinx-quickstart in a temporary directory.
    Returns the path of the project and the index file.
    """
    project_dir = os.path.join(os.getcwd(), project_name)
    index_file = os.path.join(project_dir, 'index.rst')
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)
    subprocess.run(['sphinx-quickstart', '--quiet', '--project', project_name, '--author', 'Test', project_dir], check=True)
    return project_dir, index_file

def write_index_file(index_file: str):
    """
    Writes a simple RST document with both an external and a local (broken) link to the index_file.
    """
    content = """
broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
"""
    with open(index_file, 'w') as f:
        f.write(content)

def run_linkcheck(project_dir: str) -> str:
    """
    Runs the sphinx-build command in linkcheck mode on the provided project directory.
    Returns the output of the linkcheck.
    """
    result = subprocess.run(['sphinx-build', '-b', 'linkcheck', project_dir, os.path.join(project_dir, '_build')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.stdout

def assert_local_link_checked(output: str):
    """
    Asserts that the output contains a check for the local link, raising an AssertionError if not.
    """
    if "doesntexist" not in output:
        raise AssertionError("Local link was not checked.")

def main():
    try:
        project_name = "test_project"
        project_dir, index_file = create_sphinx_project(project_name)
        write_index_file(index_file)
        output = run_linkcheck(project_dir)
        assert_local_link_checked(output)
        print("Local link is correctly checked.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    finally:
        # Optionally clean up the project directory
        pass

if __name__ == "__main__":
    main()
```

This script:
- Creates a temporary Sphinx project,
- Adds a document with bogus links (one external and one meant to be local),
- Runs the `linkcheck` build,
- Asserts whether the linkcheck output indicates a check for the local link,
- Properly reports an assertion error or any Exception stack trace if the operation does not complete as expected,
- Cleans up by removing the temporary project (note this cleanup is commented out by default; you might want to uncomment it based on how you plan to use this script).

Before running this script, make sure you have Sphinx installed (`pip install sphinx`) and that you're able to run `sphinx-quickstart` and `sphinx-build` commands from your terminal or command prompt. Adjust the script according to your environment and needs, especially if the location of binaries or the way of executing commands differs.