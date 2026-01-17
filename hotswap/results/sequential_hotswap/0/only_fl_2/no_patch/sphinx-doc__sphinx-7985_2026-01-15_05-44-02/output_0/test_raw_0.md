```python
import subprocess
import os

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

def setup_sphinx_project():
    """
    Sets up a Sphinx project environment to test the linkcheck on local links.
    """
    # Create a template Sphinx project
    project_dir = "test_sphinx_project"
    try:
        os.makedirs(project_dir)
    except FileExistsError:
        pass

    with open(os.path.join(project_dir, 'index.rst'), 'w') as f:
        f.write(
            """
broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
"""
        )

    with open(os.path.join(project_dir, 'conf.py'), 'w') as f:
        f.write(
            """
project = 'TestProject'
master_doc = 'index'
"""
        )

    return project_dir

def check_for_issues(project_dir: str):
    """
    Runs Sphinx's linkcheck and analyzes the output to determine whether local links are checked.
    """
    try:
        result = subprocess.run(["sphinx-build", "-b", "linkcheck", ".", "_build"], cwd=project_dir, capture_output=True, text=True, check=True)
        output = result.stdout
        if "broken    https://lkfqhlkghflkhs" not in output or "local-link_" not in output:
            raise AssertionError("Local link was not checked as expected.")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("Sphinx linkcheck failed to execute properly.") from e

def main():
    project_dir = setup_sphinx_project()
    try:
        check_for_issues(project_dir)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issues detected - The issue may be fixed.")
    exit(0)

if __name__ == "__main__":
    main()
```

This script does several things:
- It sets up a minimal Sphinx project with a configuration file and an `index.rst` file that contains both a broken external link and a broken internal link.
- It runs the Sphinx `linkcheck` build in the project directory and captures its output.
- If the check properly recognizes an issue with the local link (`doesntexist`), it is expected, but since the current issue complains about lack of local link checking, an `AssertionError` will be raised if the local link is not mentioned as broken in the output.
- If the Sphinx `linkcheck` does not run properly, or if the script encounters any issue executing the Sphinx build, it prints the stack trace of the exception.
- The script will exit with code 0 only if no issues are detected (meaning if local links are both checked and reported correctly in a hypothetical fixed version of Sphinx).

Note: Before running this script, ensure that Sphinx is installed in your environment (`pip install sphinx`) and that the Sphinx project setup suits the requirements (e.g., `sphinx-quickstart` might be needed for a more complete setup in a real-world scenario).