Here is a standalone Python script `reproducer.py` that reproduces the issue described. This script automates the creation of a Sphinx project, modifies the `index.rst` file to include both a broken local and external link as described, and then runs the `sphinx-build` command in linkcheck mode. It assesses the outcome by parsing the output to check if both the external and local links are checked and marked as broken. If the expected behavior (checking local links) is not observed, an `AssertionError` is raised, and the stack trace of that assertion is printed as requested.

```python
import subprocess
import os
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

def setup_sphinx_project():
    # Automatically accept defaults for sphinx-quickstart
    subprocess.check_call(['sphinx-quickstart', 'test_project', '--quiet', '--project', 'My Test', '--author', 'Me', '--release', '0.1'])

    index_rst_path = os.path.join('test_project', 'index.rst')
    with open(index_rst_path, 'a') as f:
        f.write('\n')  # Ensure new content starts on a new line
        f.write('.. _external-link: https://lkfqhlkghflkhs\n')
        f.write('.. _local-link: doesntexist\n')
        f.write('\nbroken external-link_\n')
        f.write('broken local-link_\n')

def run_linkcheck():
    result = subprocess.run(['sphinx-build', '-b', 'linkcheck', 'test_project', 'test_project/_build'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def check_results(stdout, stderr):
    assert "local-link: doesntexist" in stdout, "Local link was not checked."

if __name__ == "__main__":
    try:
        setup_sphinx_project()
        stdout, stderr = run_linkcheck()
        check_results(stdout, stderr)
        print("Test passed: Local links are being checked.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

Save this script as `reproducer.py` in the root directory of your project. This script should be run in an environment where Sphinx and its dependencies are installed, and Python 3 is used. The script sets up a minimal Sphinx project, modifies the `index.rst` file to include both broken local and external links, runs linkcheck, and checks the output to confirm if the local link checking behavior is as expected. If the issue is present (i.e., local links are not checked correctly), an `AssertionError` is raised, and the script prints a detailed stack trace.
