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
